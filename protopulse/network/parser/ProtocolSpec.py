import importlib
import json
import os
from pathlib import Path
from typing import Dict, List
from pydantic import BaseModel
from jinja2 import Template
from tqdm import tqdm

from protopulse.network.messages.INetworkMessage import INetworkMessage
from protopulse.network.parser.TypeEnum import TypeEnum


PROTOCOL = None
PRIMITIVES = ["int", "float", "bool", "str", "list", "dict", "bytearray"]
currdir = Path(os.path.dirname(__file__))

class FieldSpec(BaseModel):
    dynamicType: bool
    length: int
    lengthTypeId: int
    name: str
    optional: bool
    type: str
    typeId: TypeEnum
    typename: str

    def isPrimitive(self):
        return self.typeId != TypeEnum.OBJECT
    
    def isVector(self):
        return self.length or self.lengthTypeId

class ClassSpec(BaseModel):
    parent: str
    package: str
    name: str
    protocolId: int
    fields: List[FieldSpec] = []
    boolfields = List[FieldSpec]
    
    def importClass(self):
        try:
            self.clsModule = globals()[self.package]
        except:
            self.clsModule = importlib.import_module(self.package)
        self.cls: INetworkMessage = getattr(self.clsModule, self.name)

class ProtocolSpec(BaseModel):
    type_by_id: Dict[str, ClassSpec]
    msg_by_id: Dict[str, ClassSpec]
    type: Dict[str, ClassSpec]
            
    def getTypeSpecById(self, id):
        if str(id) not in self.type_by_id:
            raise AttributeError(f"Type id {id} not found in known types ids")
        return self.type_by_id.get(str(id))

    def getClassSpecById(self, id):
        if str(id) not in self.msg_by_id:
            raise AttributeError(f"msg id {id} not found in known msg ids")
        return self.msg_by_id.get(str(id))

    def getClassSpecByName(self, name):
        if name not in self.type:
            raise AttributeError(f"msg name {name} not found in known msg types")
        return self.type.get(name)

    def getMsgNameById(self, id):
        return self.getClassSpecById(id).name

    def getProtocolIdByName(self, name):
        return self.getClassSpecByName(name).protocolId

    @staticmethod
    def getInitArgs(spec):
        init_args = []
        nonPrimitives = []
        for field in spec["fields"]:
            if field["typename"] in PRIMITIVES:
                typename = field["typename"]
            else:
                typename = f"'{field['typename']}'"
                nonPrimitives.append(field["typename"])
            ftype = (
                typename
                if field["length"] is None and field["lengthTypeId"] is None
                else f"list[{typename}]"
            )
            init_args.append({"name": field["name"], "type": ftype})
        for field in spec["boolfields"]:
            init_args.append({"name": field["name"], "type": field["typename"]})
        return init_args, nonPrimitives

    @classmethod
    def generateClasses(cls, protocol_spec_file, dst_dir):
        with open(protocol_spec_file, "r") as f:
            spec = json.load(f)
            
        with open(currdir / "template.j2", "r") as f:
            template = Template(f.read())
            for msg in tqdm(cls.PROTOCOL["type"].values()):
                init_args, nonPrimitives = cls.getInitArgs(msg)

                super_args = []
                current = msg.get("parent")
                while current:
                    current = cls.PROTOCOL["type"][current]
                    inArgs, nonPrim = cls.getInitArgs(current)
                    nonPrimitives.extend(nonPrim)
                    super_args.extend(inArgs)
                    current = current.get("parent")

                r = template.render(
                    cls=msg,
                    types=cls.PROTOCOL["type"],
                    super_args=super_args,
                    init_args=init_args,
                    nonPrimitives=nonPrimitives,
                    primitives=cls.PRIMITIVES,
                )

                path_to = os.path.join(*([dst_dir] + msg["package"].split(".")))
                path_to = "{}.py".format(path_to)
                if not os.path.exists(Path(path_to).parent):
                    os.makedirs(Path(path_to).parent)
                with open(path_to, "w") as f:
                    f.write(r)

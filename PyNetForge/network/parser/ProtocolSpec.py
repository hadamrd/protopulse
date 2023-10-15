import importlib
import json
import os
from jinja2 import Template
from PyNetForge.network.messages.INetworkMessage import INetworkMessage
from PyNetForge.network.parser.TypeEnum import TypeEnum
from tqdm import tqdm
from pathlib import Path

class ClassSpec:
    
    def __init__(self, infos: dict) -> None:
        self.parent: str = infos.get("parent")
        self.package: str = infos.get("package")
        self.name: str = infos.get("name")
        self.protocolId: int = infos.get("protocolId")
        self.hash_function: str = infos.get("hash_function")
        self.fields = [FieldSpec(f) for f in infos.get("fields")]
        self.boolfields = [FieldSpec(f) for f in infos.get("boolfields")]
        modulePath = self.package
        try:
            self.clsModule = globals()[modulePath]
        except:
            self.clsModule = importlib.import_module(modulePath)
        self.cls: INetworkMessage = getattr(self.clsModule, self.name)
        self.json = infos
        
    def __repr__(self) -> str:
        return json.dumps(self.json)

class FieldSpec:

    def __init__(self, infos: dict):
        self.dynamicType: bool = infos.get("dynamicType")
        self.length: int = infos.get("length")
        self.lengthTypeId: int = infos.get("lengthTypeId")
        self.name: str = infos.get("name")
        self.optional: bool = infos.get("optional")
        self.type: str = infos.get("type")
        self.typeId: TypeEnum = TypeEnum(infos.get("typeId"))
        self.typename: str = infos.get("typename")
        self.json = infos

    def isPrimitive(self):
        return self.typeId != TypeEnum.OBJECT
    
    def isVector(self):
        return self.length or self.lengthTypeId
    
    def __repr__(self) -> str:
        return json.dumps(self.json)

class ProtocolSpec:
    PROTOCOL = None
    PRIMITIVES = ["int", "float", "bool", "str", "list", "dict", "bytearray"]

    @classmethod
    def load(cls, filepath):
        if not os.path.exists(filepath):
            raise Exception(f"{filepath} file not found")
        with open(filepath, "r") as fp:
            cls.PROTOCOL = json.load(fp)
            
    @classmethod
    def getTypeSpecById(cls, id):
        if str(id) not in cls.PROTOCOL["type_by_id"]:
            raise AttributeError(f"Type id {id} not found in known types ids")
        return ClassSpec(cls.PROTOCOL["type_by_id"][str(id)])

    @classmethod
    def getClassSpecById(cls, id) -> ClassSpec:
        if str(id) not in cls.PROTOCOL["msg_by_id"]:
            raise AttributeError(f"msg id {id} not found in known msg ids")
        return ClassSpec(cls.PROTOCOL["msg_by_id"][str(id)])

    @classmethod
    def getClassSpecByName(cls, name) -> ClassSpec:
        if name not in cls.PROTOCOL["type"]:
            raise AttributeError(f"msg name {name} not found in known msg types")
        return ClassSpec(cls.PROTOCOL["type"][name])

    @classmethod
    def getMsgNameById(cls, id):
        return cls.getClassSpecById(id).name

    @classmethod
    def getProtocolIdByName(cls, name):
        return cls.getClassSpecByName(name).protocolId

    @classmethod
    def getInitArgs(cls, spec):
        init_args = []
        nonPrimitives = []
        for field in spec["fields"]:
            if field["typename"] in cls.PRIMITIVES:
                typename = field["typename"]
            else:
                typename = f"'{field['typename']}'"
                nonPrimitives.append(field["typename"])
            ftype = (
                typename
                if field["length"] is None and field["lengthTypeId"] is None
                else "list[" + typename + "]"
            )
            init_args.append({"name": field["name"], "type": ftype})
        for field in spec["boolfields"]:
            init_args.append({"name": field["name"], "type": field["typename"]})
        return init_args, nonPrimitives

    @classmethod
    def generateClasses(cls, dst_dir):
        file_dir = Path(os.path.dirname(__file__))
        with open(file_dir / "template.j2", "r") as f:
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

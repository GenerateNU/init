from enum import Enum, unique

Attrset = dict[str, "NixType"]
NixType = Attrset | list["NixType"] | str | int | float | bool | None


def serialize_nix_obj(obj: NixType, *, indent: int = 2, level: int = 0) -> str:
    ind = " " * indent * level

    if isinstance(obj, dict):
        return (
            f"{{\n"
            + "".join(
                f"{ind}  {k} = {serialize_nix_obj(v, indent=indent, level=level + 1)};\n"
                for k, v in obj.items()
            )
            + f"{ind}}}"
        )
    elif isinstance(obj, list):
        return (
            f"[\n"
            + "".join(
                f"{ind}  {serialize_nix_obj(item, indent=indent, level=level + 1)}\n"
                for item in obj
            )
            + f"{ind}]"
        )
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, bool):
        return "true" if obj else "false"
    elif isinstance(obj, (float, int)):
        return str(obj)
    elif obj is None:
        return "null"
    else:
        raise TypeError(f"type must be a valid Nix type, not {type(obj).__name__}")


class NixOption:
    def __init__(
        self,
        *,
        name: str,
        nix_value: Attrset = {"enable": True},
        extra_pkgs: set[str] = set(),
    ) -> None:
        self.__name: str = name
        self.__value: Attrset = nix_value
        self.__extra_pkgs: set[str] = extra_pkgs

    def extra_pkgs(self) -> set[str]:
        return self.__extra_pkgs

    def __str__(self) -> str:
        return f"{self.__name} = {serialize_nix_obj(self.__value)};"


@unique
class Language(Enum):
    ANSIBLE = NixOption(name="ansible")
    C = NixOption(name="c")
    CLOJURE = NixOption(name="clojure")
    CPLUSPLUS = NixOption(name="cplusplus")
    CRYSTAL = NixOption(name="crystal")
    CUE = NixOption(name="cue")
    DART = NixOption(name="dart")
    DOTNET = NixOption(name="dotnet")
    ELIXIR = NixOption(name="elixir")
    ELM = NixOption(name="elm")
    ERLANG = NixOption(name="erlang")
    FORTRAN = NixOption(name="fortran")
    GAWK = NixOption(name="gawk")
    GLEAM = NixOption(name="gleam")
    GO = NixOption(name="go", extra_pkgs={"golangci-lint"})
    HASKELL = NixOption(name="haskell")
    IDRIS = NixOption(name="idris")
    JAVA = NixOption(name="java")
    JAVASCRIPT_BUN = NixOption(
        name="javascript",
        nix_value={"enable": True, "bun": {"enable": True, "install.enable": True}},
    )
    JAVASCRIPT_DENO = NixOption(name="deno")
    JAVASCRIPT_PNPM = NixOption(
        name="javascript",
        nix_value={"enable": True, "pnpm": {"enable": True, "install.enable": True}},
    )
    JSONNET = NixOption(name="jsonnet")
    JULIA = NixOption(name="julia")
    KOTLIN = NixOption(name="kotlin")
    LUA = NixOption(name="lua")
    NIM = NixOption(name="nim")
    NIX = NixOption(name="nix")
    OCAML = NixOption(name="ocaml")
    ODIN = NixOption(name="odin")
    OPENTOFU = NixOption(name="opentofu")
    PASCAL = NixOption(name="pascal")
    PERL = NixOption(name="perl")
    PHP = NixOption(name="php")
    PURESCRIPT = NixOption(name="purescript")
    PYTHON = NixOption(name="python", extra_pkgs={"black", "pyright"})
    R = NixOption(name="r")
    RACKET = NixOption(name="racket")
    RAKU = NixOption(name="raku")
    ROBOT_FRAMEWORK = NixOption(name="robotframework")
    RUBY = NixOption(name="ruby")
    RUST = NixOption(name="rust")
    SCALA = NixOption(name="scala")
    SHELL = NixOption(name="shell", extra_pkgs={"bash"})
    SOLIDITY = NixOption(name="solidity")
    STANDARD_ML = NixOption(name="standardml")
    SWIFT = NixOption(name="swift")
    TERRAFORM = NixOption(name="terraform")
    TEX_LIVE = NixOption(name="texlive")
    TYPESCRIPT = NixOption(name="typescript")
    UNISON = NixOption(name="unison")
    V = NixOption(name="v")
    VALA = NixOption(name="vala")
    ZIG = NixOption(name="zig")


@unique
class Service(Enum):
    ADMINER = NixOption(name="adminer")
    BLACKFIRE = NixOption(name="blackfire")
    CADDY = NixOption(name="caddy")
    CASSANDRA = NixOption(name="cassandra")
    CLICKHOUSE = NixOption(name="clickhouse")
    COCKROACHDB = NixOption(name="cockroachdb")
    COUCHDB = NixOption(name="couchdb")
    DYNAMODB_LOCAL = NixOption(name="dynamodb-local")
    ELASTICMQ = NixOption(name="elasticmq")
    ELASTICSEARCH = NixOption(name="elasticsearch")
    HTTPBIN = NixOption(name="httpbin")
    INFLUXDB = NixOption(name="influxdb")
    MAILHOG = NixOption(name="mailhog")
    MAILPIT = NixOption(name="mailpit")
    MEILISEARCH = NixOption(name="meilisearch")
    MEMCACHED = NixOption(name="memcached")
    MINIO = NixOption(name="minio")
    MONGODB = NixOption(name="mongodb")
    MYSQL = NixOption(name="mysql")
    NGINX = NixOption(name="nginx")
    OPENSEARCH = NixOption(name="opensearch")
    OPENTELEMETRY_COLLECTOR = NixOption(name="opentelemetry-collector")
    POSTGRESQL = NixOption(name="postgres")
    RABBITMQ = NixOption(name="rabbitmq")
    REDIS = NixOption(name="redis")
    TEMPORAL = NixOption(name="temporal")
    TYPESENSE = NixOption(name="typesense")
    VARNISH = NixOption(name="varnish")
    VAULT = NixOption(name="vault")
    WIREMOCK = NixOption(name="wiremock")

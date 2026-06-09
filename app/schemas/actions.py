from pydantic import BaseModel, Field
from typing import Literal, Union, List, Annotated

class TransferResourcesParams(BaseModel):
    target_player: str = "player1"
    gold: int = 0
    wood: int = 0
    ore: int = 0
    crystal: int = 0
    mercury: int = 0
    sulfur: int = 0
    gems: int = 0

class SetAllianceParams(BaseModel):
    target_player: str = "player1"
    duration_turns: int = 1

class AttackParams(BaseModel):
    target_player: str
    reason: str = ""

class RetreatParams(BaseModel):
    reason: str

# --- Обгортки дій ---
class TransferResourcesAction(BaseModel):
    type: Literal["transfer_resources"]
    params: TransferResourcesParams

class SetAllianceAction(BaseModel):
    type: Literal["set_alliance"]
    params: SetAllianceParams

class AttackAction(BaseModel):
    type: Literal["attack"]
    params: AttackParams

class RetreatAction(BaseModel):
    type: Literal["retreat"]
    params: RetreatParams


# --- Реєстр команд ---
GameAction = Annotated[
    Union[TransferResourcesAction, SetAllianceAction, AttackAction, RetreatAction],
    Field(discriminator="type")
]

# --- Фінальна відповідь ---
class ModelResponse(BaseModel):
    dialogue_text: str
    actions: List[GameAction] = Field(default_factory=list)
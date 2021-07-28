import fastapi
import uvicorn

from models.user_model import UserModel
from models.risk_model import RiskModel
from riskProfile import RiskProfile

app = fastapi.FastAPI(
    title="Risk Profile API",
    description='API determines the user’s insurance needs by asking personal & risk-related questions and gathering information about the user’s vehicle and house. Using this data, Origin determines their risk profile for each line of insurance and then suggests an insurance plan ("economic", "regular", "responsible") corresponding to her risk profile.',
    version="1.0"
)


@app.get("/")
def index():
    return {"message": "Hello World",
            "documentation": "Call /docs to see all the documentation"}


@app.post('/api/risk/', response_model=RiskModel)
async def calculate_user_risk(user: UserModel):
    risk_profile = RiskProfile(user)
    return risk_profile.get_risk_profile()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

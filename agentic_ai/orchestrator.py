
from datetime import datetime

from datetime import datetime

from agentic_ai.agents.market_data_agent import MarketDataAgent
from agentic_ai.agents.technical_analysis_agent import TechnicalAnalysisAgent
from agentic_ai.agents.strategy_agent import StrategyAgent
from agentic_ai.agents.risk_analysis_agent import RiskAnalysisAgent
from agentic_ai.agents.ml_prediction_agent import MLPredictionAgent
from agentic_ai.agents.decision_agent import DecisionAgent
from agentic_ai.agents.ai_explanation_agent import AIExplanationAgent
from update.update_market_data import update_market_data


class GrohmAgenticOrchestrator:

    def __init__(self):

        self.system_name = "GROHM Agentic AI"

        # Initialize all seven agents
        self.market_data_agent = MarketDataAgent()
        self.technical_agent = TechnicalAnalysisAgent()
        self.strategy_agent = StrategyAgent()
        self.risk_agent = RiskAnalysisAgent()
        self.ml_agent = MLPredictionAgent()
        self.decision_agent = DecisionAgent()
        self.explanation_agent = AIExplanationAgent()

        self.agents = [
            "Market Data Agent",
            "Technical Analysis Agent",
            "Strategy Agent",
            "Risk Analysis Agent",
            "ML Prediction Agent",
            "Decision Agent",
            "AI Explanation Agent"
        ]

    def get_system_status(self):

        return {
            "system": self.system_name,
            "status": "READY",
            "agents": self.agents,
            "total_agents": len(self.agents),
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

    def run_workflow(self, question):

        if not question or not question.strip():
           raise ValueError("Please enter a question.")

        print("GROHM: Updating latest BTCUSD data...")

        try:
            update_market_data()
            print("GROHM: Market data updated successfully.")

        except Exception as error:
            raise RuntimeError(
               f"Market data update failed: {error}"
            )

    # Continue with existing seven-agent workflow

        # 1. Market Data Agent
        market_data = self.market_data_agent.load_market_data()

        # 2. Technical Analysis Agent
        technical_analysis = self.technical_agent.analyze_market()

        # 3. Strategy Agent
        strategy_analysis = self.strategy_agent.analyze_strategy()

        # 4. Risk Analysis Agent
        risk_analysis = self.risk_agent.analyze_risk()

        # 5. ML Prediction Agent
        ml_prediction = self.ml_agent.analyze_prediction()

        # 6. Decision Agent
        decision = self.decision_agent.decide(
            market_data,
            technical_analysis,
            strategy_analysis,
            risk_analysis,
            ml_prediction
        )

        # 7. AI Explanation Agent
        explanation = self.explanation_agent.explain({
            "decision": decision,
            "technical_analysis": technical_analysis,
            "strategy_analysis": strategy_analysis,
            "risk_analysis": risk_analysis,
            "ml_prediction": ml_prediction
        })

        return {
            "system": self.system_name,
            "question": question,
            "workflow_status": "SUCCESS",
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "market_data": market_data,
            "technical_analysis": technical_analysis,
            "strategy_analysis": strategy_analysis,
            "risk_analysis": risk_analysis,
            "ml_prediction": ml_prediction,
            "decision": decision,
            "ai_explanation": explanation,
            "message": "Seven GROHM agents executed successfully."
        }
if __name__ == "__main__":

    print("=" * 50)
    print("       GROHM AGENTIC AI")
    print("=" * 50)

    orchestrator = GrohmAgenticOrchestrator()

    print("\nSystem Status:")
    print(orchestrator.get_system_status())

    print("\nStarting Agentic AI Workflow...\n")

    result = orchestrator.run_workflow("Analyze BTCUSD")

    print("\nGROHM COMPLETE OUTPUT:")
    print(result)






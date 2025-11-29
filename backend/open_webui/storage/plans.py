# data/plans.py
from uuid import UUID, uuid4
from open_webui.models.pricing import PricingPlan, PlanFeature
 
PLANS = [
    PricingPlan(
        id="basic",
        name="Basic",
        tagline="Perfect for getting started",
        price="$5",
        period="month",
        amount=5,
        group_id="d5a8957e-09e9-4cc1-88cb-41775d199c03",
        highlighted=False,
        badge=None,
        features=[
            PlanFeature(text="Coverage: Basic statutes + case law"),
            PlanFeature(text="Jurisdiction-ready citations"),
            PlanFeature(text="Expanded messaging and uploads"),
            PlanFeature(text="Longer memory and context"),
            PlanFeature(text="Limited deep research"),
            PlanFeature(text="Up to 8K context tokens / request"),
            PlanFeature(text="Access to custom prompts", coming_soon=False),
            # commented features → just set enabled=False or remove
        ],
    ),
    PricingPlan(
        id="enterprise",
        name="Enterprise",
        tagline="Advanced features for professionals",
        price="$10",
        period="month",
        amount=10,
        group_id="efb32256-b192-43c9-ab69-3273c8035608",
        highlighted=True,
        badge="Most Popular",
        features=[
            PlanFeature(text="Everything in Basic"),
            PlanFeature(text="Comprehensive legal coverage"),
            PlanFeature(text="Includes legal sources and gazettes issues"),
            PlanFeature(text="Enhanced research capabilities"),
            PlanFeature(text="Daily content updates"),
            PlanFeature(text="Citations with deep links"),
            PlanFeature(text="Expanded memory and context"),
        ],
    ),
    PricingPlan(
        id="enterprise_plus",
        name="Enterprise Plus",
        tagline="Premium solution for teams",
        price="$20",
        period="month",
        amount=20,
        group_id="acaf2c58-69c9-478c-8b38-6620c23247f9",
        highlighted=False,
        badge="Best Value",
        features=[
            PlanFeature(text="Everything in Enterprise Plan"),
            PlanFeature(text="Enhanced Models trained with Legal datasets"),
            PlanFeature(text="Models trained with court decisions"),
            PlanFeature(text="Priority support 24/7"),
            PlanFeature(text="includes Gazette issues, legal sources and Court Decisions"),
        ],
    ),
]
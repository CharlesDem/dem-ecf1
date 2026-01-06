from src.partner_pipeline import PartnerPipeline
from src.quote_pipeline import QuotePipeline


def main():
    # quote_pipeline = QuotePipeline()
    # quote_pipeline.quotes()


    partner_pipeline = PartnerPipeline()
    partner_pipeline.save_partners()

if __name__ == "__main__":
    main()
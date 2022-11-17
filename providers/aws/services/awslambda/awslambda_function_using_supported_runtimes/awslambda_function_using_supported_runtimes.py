from lib.check.models import Check, Check_Report
from providers.aws.services.awslambda.awslambda_client import awslambda_client
from config.config import get_config_var


class awslambda_function_using_supported_runtimes(Check):
    def execute(self):
        findings = []
        for function in awslambda_client.functions.values():
            report = Check_Report(self.metadata)
            report.region = function.region
            report.resource_id = function.name
            report.resource_arn = function.arn

            if function.runtime in get_config_var("obsolete_lambda_runtimes"):
                report.status = "FAIL"
                report.status_extended = f"Lambda function {function.name} is using {function.runtime} which is obsolete"
            else:
                report.status = "PASS"
                report.status_extended = f"Lambda function {function.name} is using {function.runtime} which is supported"

            findings.append(report)

        return findings
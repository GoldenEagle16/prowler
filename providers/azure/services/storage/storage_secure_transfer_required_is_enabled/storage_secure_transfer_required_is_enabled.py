from lib.check.models import Check, Check_Report
from providers.azure.services.storage.storage_client import storage_client


class storage_secure_transfer_required_is_enabled(Check):
    def execute(self) -> Check_Report:
        findings = []
        for subscription, storage_accounts in storage_client.storage_accounts.items():
            for storage_account in storage_accounts:
                report = Check_Report(self.metadata)
                report.region = storage_client.region
                report.status = "PASS"
                report.status_extended = f"Storage account {storage_account.name} from subscription {subscription} has secure transfer required enabled"
                report.resource_id = storage_account.name
                report.resource_arn = storage_account.id
                if not storage_account.enable_https_traffic_only:
                    report.status = "FAIL"
                    report.status_extended = f"Storage account {storage_account.name} from subscription {subscription} has secure transfer required disabled"

                findings.append(report)

        return findings
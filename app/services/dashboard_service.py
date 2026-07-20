class DashboardService:

    def __init__(self, repo):
        self.repo = repo

    def dashboard(self):
        return {
            "summary": self.repo.get_summary(),

            "migration_status": [
                {
                    "status": s,
                    "count": c
                }
                for s, c in self.repo.migration_chart()
            ],

            "applications_by_domain": [
                {
                    "domain": d,
                    "count": c
                }
                for d, c in self.repo.domain_chart()
            ],

            "cloud_distribution": [
                {
                    "cloud": c,
                    "count": n
                }
                for c, n in self.repo.cloud_chart()
            ],

            "recent_uploads": self.repo.recent_uploads(),

            "recent_audit_logs": self.repo.recent_logs(),
        }
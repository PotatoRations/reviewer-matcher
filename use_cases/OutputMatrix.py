
class OutputMatrix:

    def __init__(self, reviewer_assignments, applicant_assignments, reviewer_names, applicant_names) -> None:
        self.reviewer_assignments = reviewer_assignments
        self.applicant_assignments = applicant_assignments
        self.applicants = applicant_names
        self.reviewers = reviewer_names
        return
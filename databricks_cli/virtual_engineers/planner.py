# Databricks CLI
# Copyright 2017 Databricks, Inc.

from __future__ import absolute_import

import uuid

AI_ENGINEER_ROLES = [
    'AI Data Engineer',
    'AI MLOps Engineer',
    'AI DevOps Engineer',
    'AI Research Engineer',
    'AI Platform Engineer',
]

TECHNICAL_SKILLS = [
    'AWS',
    'Python',
    'Spark',
    'ETL',
    'CI/CD',
    'Kubernetes',
    'Databricks',
    'Terraform',
    'MLflow',
]

DEFAULT_TOOLCHAIN = {
    'AWS': ['CloudWatch', 'S3', 'IAM'],
    'Python': ['Pytest', 'Poetry'],
    'Spark': ['Spark SQL', 'Structured Streaming'],
    'ETL': ['Airflow', 'dbt'],
    'CI/CD': ['GitHub Actions', 'Jenkins'],
    'Kubernetes': ['Helm', 'Prometheus'],
    'Databricks': ['Jobs', 'Delta Live Tables', 'Unity Catalog'],
    'Terraform': ['Terraform Cloud'],
    'MLflow': ['Model Registry', 'Tracking Server'],
}


def _normalize_list(raw_value):
    if raw_value is None:
        return []
    if isinstance(raw_value, list):
        return [item for item in raw_value if item]
    return [raw_value]


def build_engineer_blueprint(request_data):
    company = request_data.get('company_name') or request_data.get('full_name') or 'Unknown Organization'
    role = request_data.get('role') or AI_ENGINEER_ROLES[0]
    skills = _normalize_list(request_data.get('skills'))
    responsibilities = _normalize_list(request_data.get('responsibilities'))

    selected_tooling = []
    for skill in skills:
        selected_tooling.extend(DEFAULT_TOOLCHAIN.get(skill, []))

    if not responsibilities:
        responsibilities = [
            'Build and orchestrate resilient data and ML workflows.',
            'Monitor systems and proactively remediate incidents.',
            'Generate engineering and compliance reports for stakeholders.',
        ]

    orchestration_plan = {
        'planner_agent': 'Builds task plans from stakeholder requests and long-term memory.',
        'executor_agent': 'Runs automated jobs and infrastructure workflows using approved tools.',
        'quality_agent': 'Performs test, data quality, and reliability checks before completion.',
        'reporter_agent': 'Generates human-readable updates and audit logs.',
    }

    return {
        'engineer_id': str(uuid.uuid4()),
        'organization': company,
        'role': role,
        'skills': skills,
        'responsibilities': responsibilities,
        'tooling': sorted(set(selected_tooling)),
        'memory_profile': {
            'short_term': 'Session memory for active workflow context.',
            'long_term': 'Vector memory for runbooks, architecture decisions, and incidents.',
        },
        'orchestration': orchestration_plan,
        'deployment': {
            'status': 'deployed',
            'execution_mode': 'autonomous-with-human-approval-gates',
        },
    }

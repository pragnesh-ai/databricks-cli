from databricks_cli.virtual_engineers.planner import build_engineer_blueprint


def test_build_engineer_blueprint_uses_supplied_inputs():
    payload = {
        'company_name': 'Acme Labs',
        'role': 'AI MLOps Engineer',
        'skills': ['Python', 'Databricks'],
        'responsibilities': ['Ship CI/CD pipelines', 'Monitor model drift'],
    }

    blueprint = build_engineer_blueprint(payload)

    assert blueprint['organization'] == 'Acme Labs'
    assert blueprint['role'] == 'AI MLOps Engineer'
    assert blueprint['skills'] == ['Python', 'Databricks']
    assert 'Jobs' in blueprint['tooling']
    assert blueprint['deployment']['status'] == 'deployed'


def test_build_engineer_blueprint_supplies_defaults():
    blueprint = build_engineer_blueprint({'full_name': 'Avery'})

    assert blueprint['organization'] == 'Avery'
    assert blueprint['role']
    assert len(blueprint['responsibilities']) >= 1
    assert blueprint['orchestration']['planner_agent']

"""Read-only source-lineage analysis for UG-001.

A shared upstream is evidence of possible dependence, not proof of copying.
Unknown upstream is not proof of independence. This module does not authenticate sources.
"""


def lineage_assessment(connection, claim_a, claim_b):
    """Return a bounded documentary assessment for two claim identifiers."""
    rows = connection.execute('''
        SELECT c.id, c.source_id, s.upstream
        FROM claim AS c JOIN source AS s ON s.id = c.source_id
        WHERE c.id IN (?, ?) ORDER BY c.id
    ''', (claim_a, claim_b)).fetchall()
    if claim_a == claim_b or len(rows) != 2:
        return {'status': 'INCONCLUSIVE', 'reason': 'Two distinct existing claims required', 'sources': rows}
    first, second = rows
    if first[1] == second[1]:
        reason = 'Both claims cite the same source; not independent witnesses'
        status = 'SHARED_SOURCE'
    elif not first[2] or not second[2]:
        reason = 'Upstream lineage incomplete; independence unknown'
        status = 'INCONCLUSIVE'
    elif first[2] == second[2]:
        reason = 'Different sources report the same upstream; possible common-origin dependence'
        status = 'SHARED_UPSTREAM'
    else:
        reason = 'Distinct declared upstream labels; independence remains unverified'
        status = 'INCONCLUSIVE'
    return {'status': status, 'reason': reason, 'sources': rows}

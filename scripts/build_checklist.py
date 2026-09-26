"""Maintain Markdown and bundled YAML from the same reviewed checklist items."""
from pathlib import Path
import yaml

NOTICE = 'Last reviewed 2026-09-26. Not legal advice. Laws change; confirm with counsel.'
CFR = 'https://www.ecfr.gov/current/title-47/section-64.1200'
FCC = 'https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf'
FTC = 'https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule'
GROUPS = [
('Before you dial', [
('scope', 'Classify the campaign and technology', 'Document the seller, purpose, destination type, and whether the call uses an autodialer or artificial or prerecorded voice. Have counsel evaluate the actual equipment and exemptions; a product label is not a legal classification.', '47 CFR 64.1200(a)(1)-(3), (f)(2), (f)(12)', CFR),
('consent_type', 'Choose the applicable consent standard', 'Covered non-telemarketing artificial/prerecorded voice or autodialed calls to wireless numbers generally require prior express consent, subject to applicable exceptions. Commercial telemarketing calls using those technologies to wireless numbers generally require prior express written consent. Do not treat an inquiry or purchased lead as written consent.', '47 CFR 64.1200(a)(1)-(2)', CFR),
('written_consent', 'Review the written agreement', 'For covered telemarketing, preserve the signed written agreement, authorized telephone number, seller authorization and clear disclosure of artificial/prerecorded voice or autodialer calls. Consent cannot be required as a condition of purchase. Ask counsel to validate the actual form and signature evidence.', '47 CFR 64.1200(f)(9), (a)(2)', CFR),
('residential', 'Review residential artificial-voice calls separately', 'Telemarketing artificial/prerecorded voice calls to residential lines generally require prior express written consent. Non-telemarketing exceptions have their own conditions; do not transfer a wireless analysis without review.', '47 CFR 64.1200(a)(3)', CFR),
('evidence', 'Preserve consent evidence', 'Operational control: retain the exact disclosure version, timestamp with offset, source, phone, seller identity and retrievable signature/evidence reference. Optional IP and user-agent fields do not prove consent by themselves. The supplied schema checks structure only.', '47 CFR 64.1200(f)(9), (c)(2)(ii)', CFR),
]),
('AI voice specifics', [
('ai_voice', 'Treat AI-generated voices as artificial voices', 'FCC Declaratory Ruling FCC 24-17, adopted February 2 and released February 8, 2024, confirms that AI-generated human voices fall within the TCPA artificial-voice restrictions. Live generation or a conversational interface does not remove those restrictions.', 'FCC 24-17, paragraphs 1 and 4-6', FCC),
('ai_review', 'Approve the AI use case before launch', 'Operational control: review the complete interaction, including generated speech, transfers and voicemail, against the applicable consent and identification requirements. Do not read the ruling as either a blanket ban on all AI calls or blanket permission after a checkbox.', 'FCC 24-17; 47 CFR 64.1200(a), (b)', FCC),
]),
('Calling hours', [
('hours', 'Enforce called-party local hours', 'Telephone solicitations to residential subscribers may not be placed before 8 a.m. or after 9 p.m. at the called party location. Apply the wireless provisions where applicable. This toolkit conservatively excludes exactly 9 p.m. and can narrow the daily window.', '47 CFR 64.1200(c)(1), (e)', CFR),
('location', 'Verify location and stricter schedules', 'Operational control: verify the called party location; an area code is only a hint because people move and travel. Use a verified IANA timezone override where available. Recheck at dispatch, apply all candidate zones, and block unknown zones. A time pass does not authorize a call.', '47 CFR 64.1200(c)(1)', CFR),
]),
('National DNC Registry and internal DNC list', [
('national_dnc', 'Perform the separate National Registry check', 'Apply the National DNC restrictions and have counsel document any exception. For the routine-compliance error defense, the rule specifies a Registry version obtained no more than 31 days before calling, plus documented procedures. Internal-list scrubbing here does not query the Registry.', '47 CFR 64.1200(c)(2), especially (c)(2)(i)(D)', CFR),
('registry_access', 'Arrange authorized Registry access', 'Obtain access through the FTC telemarketing.donotcall.gov portal with a subscription account and applicable seller permissions. Do not reuse another seller access improperly. Record access and scrub dates.', '47 CFR 64.1200(c)(2)(i)(D)-(E); FTC Telemarketing Sales Rule guidance', FTC),
('internal_policy', 'Publish and train on an internal DNC policy', 'Maintain a written DNC policy available on demand, train personnel, and implement the company-specific suppression process. Covered artificial/prerecorded residential exemption calls also have DNC procedures.', '47 CFR 64.1200(d)(1)-(2)', CFR),
('internal_requests', 'Capture requests at receipt', 'Record the request and telephone number when received, plus the name if provided. Honor covered requests within a reasonable time, no later than ten business days. Operational control: suppress immediately and propagate to the seller systems and authorized vendors.', '47 CFR 64.1200(d)(3)', CFR),
('internal_retention', 'Maintain internal suppression records', 'Covered company-specific DNC requests must be honored for five years. Do not assume a continuing customer relationship overrides a seller-specific request. Review sharing and affiliated-entity scope before distributing suppression records.', '47 CFR 64.1200(d)(3), (d)(5)-(6), (f)(5)(i)', CFR),
]),
('Identification and opt-out for artificial voice messages', [
('identity', 'Identify the responsible entity', 'At the beginning, clearly state the responsible entity identity, including its registered business name when applicable. During or after the message, give the required contact number; observe the callback and charge restrictions.', '47 CFR 64.1200(b)(1)-(2)', CFR),
('interactive_optout', 'Test the live opt-out mechanism', 'For messages covered by (b)(3), including telemarketing artificial/prerecorded voice messages, provide automated interactive voice and/or keypress opt-out with instructions within two seconds after identification. The mechanism must automatically record the number on the DNC list and immediately end the call.', '47 CFR 64.1200(b)(3)', CFR),
('voicemail', 'Test voicemail opt-out', 'For covered messages left on voicemail or answering machines, include a toll-free callback number connecting directly to the automated opt-out mechanism so the number is automatically recorded on the DNC list.', '47 CFR 64.1200(b)(3)', CFR),
]),
('Caller ID', [
('caller_id', 'Transmit required caller identification', 'Telemarketing callers covered by this rule must transmit caller identification and may not block it. Ensure the provided number accepts DNC requests during regular business hours; review allowed seller-number substitution and exemptions.', '47 CFR 64.1601(e)', 'https://www.ecfr.gov/current/title-47/section-64.1601'),
]),
('Revocation of consent', [
('revocation', 'Accept reasonable revocation methods', 'Covered consent may be revoked through reasonable methods, not only a caller-selected channel. Operational control: capture spoken opt-outs, designated channels and other reasonable requests; stop queued calls immediately and record the request and handling evidence.', '47 CFR 64.1200(a)(10)-(11); FCC 24-24', CFR),
('revocation_review', 'Review current revocation scope and effective dates', 'Have counsel check current rules, waivers and orders for the campaign, including cross-category handling. Do not infer an operational deadline or exemption from the schema. A populated revoked_at field is historical evidence, not permission to call.', '47 CFR 64.1200(a)(10)-(12); FCC 24-24', CFR),
]),
('State laws', [
('state_review', 'Check every state you call', 'Several states impose stricter calling hours, registration or consent rules. Check each state you call and the caller jurisdiction with counsel before launch. Federal review alone is insufficient; this project deliberately supplies no state rules table or state-specific legal settings.', 'FCC 03-153, paragraphs 81-84; FTC Telemarketing Sales Rule guidance on state law', FTC),
]),
('Vendor and AI agent script review', [
('vendors', 'Assign seller and vendor responsibilities', 'Operational control: identify who obtains consent, maintains evidence, performs National Registry checks, updates internal suppression, handles revocation and responds to complaints. Verify actual behavior with test calls before enabling a campaign.', '47 CFR 64.1200(c)(2)(i), (d)(3)', CFR),
('scripts', 'Review every script branch', 'Operational control: approve opening identity, contact number, opt-out instructions, generated responses, voicemail and transfer branches. Test that an opt-out works without a human agent and that queued attempts are suppressed. Reapprove material script or vendor changes.', '47 CFR 64.1200(b)(1)-(3), (d)', CFR),
]),
('Audit trail', [
('audit', 'Make decisions reproducible', 'Operational control: retain UTC check time, verified timezone source, configured window, list versions, result, consent evidence reference, script version and reviewer. Store evidence securely with access controls and a counsel-approved retention schedule. The CLI does not maintain this audit system.', '47 CFR 64.1200(c)(2)(i), (d)(6), (f)(9)', CFR),
('release', 'Require human campaign approval', 'Operational control: record owner, review date, unresolved issues and counsel decisions before dispatch. Completed checklist statuses and passing software checks are not a legal clearance or a determination of valid consent.', '47 CFR 64.1200(a)-(d)', CFR),
])]

def main():
    groups=[]
    text=['# TCPA, DNC and calling-hours checklist', '', NOTICE, '',
          'Use this as a campaign review worksheet. Items labeled operational control are suggested implementation practices, not independent statements of law. Scope and exceptions require review. Keep status, owner and evidence in your own audit system.', '']
    for title, rows in GROUPS:
        text += ['## '+title, '']
        items=[]
        for ident, heading, detail, citation, url in rows:
            items.append(dict(id=ident,title=heading,detail=detail,citation=citation,url=url))
            text += [f'- [ ] **{ident}: {heading}.** {detail} [{citation}]({url})', '']
        groups.append(dict(title=title,items=items))
    text += [NOTICE, '']
    Path('CHECKLIST.md').write_text('\n'.join(text))
    data=yaml.safe_dump(dict(last_reviewed='2026-09-26',notice=NOTICE,groups=groups),sort_keys=False,allow_unicode=False)
    Path('checklist.yaml').write_text(data)
    Path('tcpa_toolkit/data/checklist.yaml').write_text(data)

if __name__ == '__main__':
    main()

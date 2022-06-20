import render
import unittest as ut


class TestDeriveResourceName(ut.TestCase):
    def test_all(self):
        test_cases = [
            ('opc_compute_image_list_entry', 'Oracle: opc_compute_image_list_entry', 'opc_compute_image_list_entry'),
            ('terraform_remote_state', 'Terraform: terraform_remote_state', 'remote_state'),
            ('tls_self_signed_cert', 'tls_self_signed_cert Resource - terraform-provider-tls', 'tls_self_signed_cert (Resource)'),
            ('ad_gpo', 'ad_gpo Data Source - terraform-provider-ad', 'ad_gpo (Data Source)'),
            ('archive_file', 'Archive: archive_file', 'archive_file'),
            ('aws_acm_certificate', 'AWS: aws_acm_certificate', 'Resource: aws_acm_certificate'),
            ('awscc_acmpca_certificate_authority', 'awscc_acmpca_certificate_authority Resource - terraform-provider-awscc', 'awscc_acmpca_certificate_authority (Resource)'),
            ('external', 'External Data Source', 'External Data Source'),
            ('null_data_source', 'null_data_source Data Source - terraform-provider-null', 'null_data_source'),
            ('vault_identity_oidc_key', 'Vault: vault_identity_oidc_key resource', 'vault_identity_oidc_key'),
            ('azuread_application_password', '', 'Resource: azuread_application_password'),
            ('hcp_consul_cluster_root_token', 'Resource hcp_consul_cluster_root_token - terraform-provider-hcp', 'Resource (hcp_consul_cluster_root_token)'),
            ('http', 'HTTP Data Source', 'http Data Source'),
            ('vault_transit_encrypt', 'Vault: vault_transit_encrypt data source', 'vault_transit_encrypt'),
            ('vsphere_role', 'VMware vSphere: Role', 'vsphere_role'),
            ('splunk_data_ui_views', '', 'Resource: splunk_data_ui_views'),
            ('cloudflare_access_application', 'cloudflare_access_application Resource - Cloudflare', 'cloudflare_access_application (Resource)'),
        ]

        for expect, metadata, title in test_cases:
            actual = render.derive_resource_name(metadata, title)
            self.assertEqual(actual, expect)


class TestWrapBlocks(ut.TestCase):
    def test_wrap_single_line_warning(self):
        input = '''
# foo

~> **Note:** You can specify `encrypted` or `snapshot_id` but not both.

# bar
'''

        expect = '''
# foo

<div class="alert alert-warning" markdown="1">
<div class="alert-title" markdown="1">
Note:
</div>
You can specify `encrypted` or `snapshot_id` but not both.
</div>

# bar
'''

        actual = render.wrap_blocks(input)
        self.assertEqual(expect, actual)

    def test_wrap_note_with_no_title(self):
        input = '''
# foo

-> The below configuration uses [`depends_on`](https://www.terraform.io/language/meta-arguments/depends_on) to prevent ordering issues with API Gateway automatically creating the log group first and a variable for naming consistency. Other ordering and naming methodologies may be more appropriate for your environment.

# bar
'''

        expect = '''
# foo

<div class="alert alert-note" markdown="1">
The below configuration uses [`depends_on`](https://www.terraform.io/language/meta-arguments/depends_on) to prevent ordering issues with API Gateway automatically creating the log group first and a variable for naming consistency. Other ordering and naming methodologies may be more appropriate for your environment.
</div>

# bar
'''

        actual = render.wrap_blocks(input)
        self.assertEqual(actual, expect)

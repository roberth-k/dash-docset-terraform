import render
import unittest as ut


class TestDeriveResourceName(ut.TestCase):
    def test_all(self):
        test_cases = [
            ('opc_compute_image_list_entry', 'Oracle: opc_compute_image_list_entry', 'opc_compute_image_list_entry', ''),
            ('terraform_remote_state', 'Terraform: terraform_remote_state', 'remote_state', ''),
            ('tls_self_signed_cert', 'tls_self_signed_cert Resource - terraform-provider-tls', 'tls_self_signed_cert (Resource)', ''),
            ('ad_gpo', 'ad_gpo Data Source - terraform-provider-ad', 'ad_gpo (Data Source)', ''),
            ('archive_file', 'Archive: archive_file', 'archive_file', ''),
            ('aws_acm_certificate', 'AWS: aws_acm_certificate', 'Resource: aws_acm_certificate', ''),
            ('awscc_acmpca_certificate_authority', 'awscc_acmpca_certificate_authority Resource - terraform-provider-awscc', 'awscc_acmpca_certificate_authority (Resource)', ''),
            ('external', 'External Data Source', 'External Data Source', ''),
            ('null_data_source', 'null_data_source Data Source - terraform-provider-null', 'null_data_source', ''),
            ('vault_identity_oidc_key', 'Vault: vault_identity_oidc_key resource', 'vault_identity_oidc_key', ''),
            ('azuread_application_password', '', 'Resource: azuread_application_password', ''),
            ('hcp_consul_cluster_root_token', 'Resource hcp_consul_cluster_root_token - terraform-provider-hcp', 'Resource (hcp_consul_cluster_root_token)', ''),
            ('http', 'HTTP Data Source', 'http Data Source', ''),
            ('vault_transit_encrypt', 'Vault: vault_transit_encrypt data source', 'vault_transit_encrypt', ''),
            ('vsphere_role', 'VMware vSphere: Role', 'vsphere_role', ''),
            ('splunk_data_ui_views', '', 'Resource: splunk_data_ui_views', ''),
            ('cloudflare_access_application', 'cloudflare_access_application Resource - Cloudflare', 'cloudflare_access_application (Resource)', ''),
            ('databricks_obo_token', '', 'databricks_obo_token Resource', ''),
            ('databricks_mws_workspaces', '', 'databricks_mws_workspaces resource', ''),
            ('akamai_appsec_security_policy', 'Akamai: SecurityPolicy', '', ''),
            ('nexus_repository_pypi_group', 'Resource nexus_repository_pypi_group', 'Resource nexus_repository_pypi_group', ''),
            ('azuredevops_serviceendpoint_github', 'AzureDevops: Data Source: azuredevops_serviceendpoint_github', 'Data Source : azuredevops_serviceendpoint_github', ''),
            ('google_cloud_run_v2_job_iam', '', '', '/Users/redacted/src/gh/roberth-k/dash-docset-terraform/.build/1.3.9.230305/Terraform.docset/Contents/Resources/Documents/providers/hashicorp/google/latest/docs/resources/cloud_run_v2_job_iam.html'),
            ('oci_core_instance', 'Oracle: oci_core_instance', 'oci_core_instance', '')
        ]

        for expect, metadata, title, output_file in test_cases:
            actual = render.derive_resource_name(metadata, title, output_file)
            self.assertEqual(actual, expect)


class TestAdmonitions(ut.TestCase):
    def test_admonitions_1(self):
        input = '''-> **title:** text'''
        expect = '''.. note:: title
    text'''
        actual = render.admonitions(input)
        self.assertEqual(expect, actual)

    def test_admonitions_2(self):
        input = '''
# example

-> **title:** text

~> **title2:** text2

~> text3

'''

        expect = '''
# example

.. note:: title
    text

.. warning:: title2
    text2

.. warning:: warning
    text3

'''
        actual = render.admonitions(input)
        self.assertEqual(expect, actual)

    def test_admonitions_multiline(self):
        input = '''
Preceding paragraph.
Contains multiple lines.

-> **Hold up!:** This is a
multiline admonition
   with a title.

Middle paragraph.
Also contains multiple lines.

-> This is a multiline admonition.
It has no title.

Final paragraph.
This, too, contains multiple lines.
'''

        expect = '''
Preceding paragraph.
Contains multiple lines.

.. note:: Hold up!
    This is a multiline admonition with a title.

Middle paragraph.
Also contains multiple lines.

.. note:: note
    This is a multiline admonition. It has no title.

Final paragraph.
This, too, contains multiple lines.
'''
        actual = render.admonitions(input)
        self.assertEqual(expect, actual)

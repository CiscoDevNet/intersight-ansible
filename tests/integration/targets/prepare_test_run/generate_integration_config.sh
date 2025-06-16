#!/usr/bin/env bash
# This script creates a private key PEM file and integration_config.yml with vars to include for ansible_test run
set -e

# Define file paths relative to workspace
readonly TEMPLATE_FILE="./tests/integration/targets/prepare_test_run/integration_config.yml.tpl"
readonly OUTPUT_FILE="./tests/integration/targets/prepare_test_run/integration_config.yml"
readonly PRIVATE_KEY_FILE="./tests/integration/targets/prepare_test_run/api_private_key.pem"

echo "${API_PRIVATE_KEY}" > "$PRIVATE_KEY_FILE"
echo "Private key written to ${PRIVATE_KEY_FILE}"

# Export the relative path to the key file for envsubst.
API_PRIVATE_KEY_PATH="./targets/prepare_test_run/api_private_key.pem" 
export API_PRIVATE_KEY_PATH

# Use envsubst to replace only the specified variables in the template.
# shellcheck disable=SC2016
envsubst '${API_PRIVATE_KEY_PATH},${API_KEY_ID}' < "$TEMPLATE_FILE" > "$OUTPUT_FILE"

echo "Successfully generated ${OUTPUT_FILE}"

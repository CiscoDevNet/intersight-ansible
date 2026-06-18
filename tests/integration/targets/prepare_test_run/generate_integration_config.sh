#!/usr/bin/env bash
# This script creates a private key PEM file and integration_config.yml with vars to include for ansible_test run
set -e

# Define file paths relative to workspace
readonly TEMPLATE_FILE="./tests/integration/targets/prepare_test_run/integration_config.yml.tpl"
readonly OUTPUT_FILE="./tests/integration/targets/prepare_test_run/integration_config.yml"
readonly PRIVATE_KEY_FILE="./tests/integration/targets/prepare_test_run/api_private_key.pem"

API_KEY_ID="${API_KEY_ID:-${INTERSIGHT_API_KEY_ID:-${INTERSIGHT_API_KEY_ID_CI:-}}}"
API_PRIVATE_KEY="${API_PRIVATE_KEY:-${INTERSIGHT_API_PRIVATE_KEY:-${INTERSIGHT_API_PRIVATE_KEY_CI:-}}}"
export API_KEY_ID
export API_PRIVATE_KEY

if [[ -z "${API_KEY_ID}" || -z "${API_PRIVATE_KEY}" ]]; then
  echo "API credentials are required. Set API_KEY_ID/API_PRIVATE_KEY or INTERSIGHT_API_KEY_ID/INTERSIGHT_API_PRIVATE_KEY." >&2
  exit 1
fi

private_key_source="${API_PRIVATE_KEY}"
if [[ "${private_key_source}" == "~/"* ]]; then
  private_key_source="${HOME}/${private_key_source#~/}"
fi

if [[ -f "${private_key_source}" ]]; then
  cp "${private_key_source}" "$PRIVATE_KEY_FILE"
else
  printf '%s\n' "${API_PRIVATE_KEY}" > "$PRIVATE_KEY_FILE"
fi
echo "Private key written to ${PRIVATE_KEY_FILE}"

# Export the relative path to the key file for envsubst.
API_PRIVATE_KEY_PATH="./targets/prepare_test_run/api_private_key.pem" 
export API_PRIVATE_KEY_PATH

# Use envsubst to replace only the specified variables in the template.
# shellcheck disable=SC2016
envsubst '${API_PRIVATE_KEY_PATH},${API_KEY_ID}' < "$TEMPLATE_FILE" > "$OUTPUT_FILE"

echo "Successfully generated ${OUTPUT_FILE}"

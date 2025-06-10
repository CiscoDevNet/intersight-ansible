#!/usr/bin/env bash

# This script creates a file for the private key, substitutes its relative path
# into the template file, and creates the final configuration file.

set -e # Exit immediately if a command exits with a non-zero status.

# Define file paths relative to the collection root
readonly TEMPLATE_FILE="./integration_config.yml.tpl"
readonly OUTPUT_FILE="./integration_config.yml"
readonly PRIVATE_KEY_FILE="./api_private_key.pem"

# 1. Write the private key from the environment variable to its own file.
echo "${API_KEY_ID}" > "$PRIVATE_KEY_FILE"
echo "Private key written to ${PRIVATE_KEY_FILE}"

# 2. Export the relative path to the key file for envsubst.
# Since the output config and the key file are in the same directory,
# the relative path is just the filename.
API_PRIVATE_KEY_PATH="./$(basename "$PRIVATE_KEY_FILE")"
export API_PRIVATE_KEY_PATH

# 3. Use envsubst to replace only the specified variables in the template.
# This prevents other text with '$' from being accidentally substituted.
# shellcheck disable=SC2016
envsubst '${API_PRIVATE_KEY_PATH},${API_KEY_ID}' < "$TEMPLATE_FILE" > "$OUTPUT_FILE"

echo "Successfully generated ${OUTPUT_FILE}"

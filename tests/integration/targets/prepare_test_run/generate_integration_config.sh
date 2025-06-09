#!/usr/bin/env bash

# This script substitutes environment variables into the template file
# and creates the final configuration file.

set -e # Exit immediately if a command exits with a non-zero status.

# Define file paths relative to the collection root
TEMPLATE_FILE="./tests/integration/targets/prepare_test_run/integration_config.yml.tpl"
OUTPUT_FILE="./tests/integration/targets/prepare_test_run/integration_config.yml"

# Use envsubst to replace ${API_PRIVATE_KEY} and ${API_KEY_ID}
# with their values from the environment.
envsubst < "$TEMPLATE_FILE" > "$OUTPUT_FILE"

echo "Successfully generated ${OUTPUT_FILE}"
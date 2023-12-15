The purpose of the unit tests is to ensure that each unit/section of the workflow works as expected. In this project, I have employed auto-generated unit test. Full details about the tests for this project can be found in the [tests branch](https://github.com/ibuliyaminu/Computational_Workflow_Project_for_2D_Materials/tree/Test/snakemake_envr/.tests/unit) on Github. But, I will give a short explanation below.

## Step 1

:::test_create_BULK_d12_from_cif.test_create_BULK_d12_from_cif

This checks the functionality of the conversion of cif file to d12 file. The function takes some parameters from the input file (**WTe2**) to generate the output file (**.d12**) as expected. It has been confirmed that this part works fine.

## Step 2

:::test_check_errored_output.test_check_errored_output

After the optimization step has been completed, the next step is to confirm if there is any error in the output file. So, this section of the test confirms the functionality of the code. It has been confirmed that this section also works fine.

## Step 3

:::test_convert_output_to_cif.test_convert_output_to_cif

After the optimization, the output structure has to be vizualized. To achieve this, the output file (**.out**) must be converted to cif file (**.cif**). As expected, this section also works well.

# APIs instructions

## Status of Task

We neeed to have run and tasks ids.

1. Get all DAG:

   - api: `/api/v1/dags`
   - header
     - Content-Type : application/json
     - Accept : application/json
   - note: important to pass user credentials (basic auth)

2. Get all runs:

   - api: `/api/v1/dags/{dag_id}/dagRuns`
   - header
     - Content-Type : application/json
     - Accept : application/json
   - note: important to pass user credentials (basic auth)

3. Get one DAG run:
   - api: `/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}`
   - The run status is visible in the field `state`
   - header
     - Content-Type : application/json
     - Accept : application/json
   - note: important to pass user credentials (basic auth)

## Restart run from specific task

We can just restart tasks, which are still running or failed.

### Set tasks to state 'failed' (for testing)

1. Set tasks state to failed:

   - api: `api/v1/dags/{dag_id}/updateTaskInstancesState`
   - header
     - Content-Type : application/json
     - Accept : application/json
   - body:
     ```json
     {
       "dry_run": false,
       "task_id": "task_id_which_state_will_be_changed",
       "execution_date": "when_the_run_happened",
       "include_upstream": false,
       "include_downstream": true,
       "include_future": true,
       "include_past": false,
       "new_state": "failed"
     }
     ```
   - note: important to pass user credentials (basic auth)

1. Clear failed or running tasks. The tasks will be rerun automatically when the state is cleared:

   - api: `/api/v1/dags/{dag_id}/clearTaskInstances`
   - header
     - Content-Type : application/json
     - Accept : application/json
   - body:

   ```json
   {
     "dry_run": true,
     "start_date": "the_date_of_the_earliest_run_we_want_to_clear",
     "end_date": "the_date_of_the_latest_run_we_want_to_clear",
     "reset_dag_runs": true
   }
   ```

   If you want to clear just one specific task, need to add task ids in the body:

   ```json
   {
     "dry_run": false,
     "task_ids": ["save_json_in_s3", "taks_id_1", "taks_id_2"],
     "start_date": "the_date_of_the_earliest_run_we_want_to_clear",
     "end_date": "the_date_of_the_latest_run_we_want_to_clear",
     "reset_dag_runs": true
   }
   ```

   - note: important to pass user credentials (basic auth). By default, it cleans just failed tasks. More information: [here](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_clear_task_instances)

## Restart a run from the beginning

1. Restart run from the beggining:
   - api: `/api/v1/dags/aps_pull_api/dagRuns`
   - header
     - Content-Type : application/json
     - Accept : application/json
   - body:
     ```json
     {
       "dag_run_id": "string",
       "logical_date": "date_when_we_want_to_start_run",
       "conf": {}
     }
     ```
   - note: important to pass user credentials (basic auth), the logical_date has to be the future date, otherwise, the run will be queued but will never start.

## Restart a run from the beginning with specific parameters

Same as Restart a run from the beginning, just passing wanted parameters in conf field:

1. Restart run from the beggining:
   - api: `/api/v1/dags/aps_pull_api/dagRuns`
   - header
     - Content-Type : application/json
     - Accept : application/json
   - body:
     ```json
     {
       "dag_run_id": "string",
       "logical_date": "date_when_we_want_to_start_run",
       "conf": {
         "start_date": "2022-06-17",
         "until_date": "2022-06-21"
       }
     }
     ```
   - note: important to pass user credentials (basic auth), the logical_date has to be the future date, otherwise, the run will be queued but will never start.

More information about airflow apis: `https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#section/Overview`

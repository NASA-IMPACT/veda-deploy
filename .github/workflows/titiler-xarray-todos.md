Todos:
- [ ] Need to add TITILER_XARRAY_GIT_REF to environment vars
- [ ] Need to add TITILER_XARRAY_DEPLOYMENT_SECRET name to environment vars and file to AWS
- [ ] update `uses: "./titiler-xarray/.github/actions/cdk-deploy"` in deploy.yml to match what Henry creates in titiler-xarray

Questions:
- [ ] is it preferred to have an option `${{ vars.TITILER_XARRAY_DEPLOYMENT_SECRET || vars.DEPLOYMENT_ENV_SECRET_NAME }}` or one or the other? Seems confusing to have both. The latter could be dangerous since it may alter existing secrets.

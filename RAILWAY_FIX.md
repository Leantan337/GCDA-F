# Fixing Django Settings Module Error on Railway

This guide addresses the specific error:
```
ModuleNotFoundError: No module named 'config.settings.production'; 'config.settings' is not a package
```

## Required Actions

### 1. Update Environment Variables in Railway Dashboard

1. Log in to your Railway dashboard
2. Open your GCDA project
3. Go to the "Variables" tab
4. Add or update the following environment variable:
   - Key: `DJANGO_SETTINGS_MODULE`
   - Value: `config.settings`

This will explicitly tell Django which settings module to use, overriding any hardcoded values.

### 2. Check Start Command

1. In your Railway dashboard, go to the "Settings" tab
2. Under "Start Command", verify it's set to:
   ```
   gunicorn config.wsgi:application
   ```
3. Ensure there are no additional environment variables being set here

### 3. Force Rebuild

Sometimes Railway needs a forced rebuild to clear any cached configurations:

1. In your Railway dashboard, go to your deployment
2. Click the "Deployments" tab
3. Click "Deploy Now" to force a new deployment with the updated environment variables

### 4. Check Service Logs

After redeploying, check the logs to see if the error persists.

## Final Check

If the error still occurs, try these additional steps:

1. Create a simple test file in your project to print the environment variables:

```python
# test_env.py
import os
print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
```

2. Add a command to run this in your Procfile:
```
web: python test_env.py && gunicorn config.wsgi:application
```

This will help verify what settings module is actually being used at runtime.

Remember to remove this test code after debugging is complete.

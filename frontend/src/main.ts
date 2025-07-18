import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
// The fix is changing 'App' to 'AppComponent' on the next line
import { AppComponent } from './app/app';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
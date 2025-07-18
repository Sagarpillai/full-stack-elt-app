import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { HistoryComponent } from './pages/history/history';
import { DataViewerComponent } from './pages/data-viewer/data-viewer';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'history', component: HistoryComponent },
  { path: 'view/:tableName', component: DataViewerComponent }
];
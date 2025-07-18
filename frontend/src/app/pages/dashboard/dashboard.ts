import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BackendService } from '../../services/backend';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent {
  statusMessage: string | null = null;
  isLoading = false;

  constructor(private backendService: BackendService) {}

  onTriggerJob(): void {
    this.isLoading = true;
    this.statusMessage = 'Processing...';

    this.backendService.triggerJob().subscribe(response => {
      console.log("Response from backend:", response); // Add this line
      this.isLoading = false;
      this.statusMessage = response.message;
    });
  }
}
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // Import this
import { BackendService } from '../../services/backend';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, RouterModule], // Add RouterModule here
  templateUrl: './history.html',
  styleUrls: ['./history.css']
})
export class HistoryComponent implements OnInit {
  jobHistory: any[] = [];
  isLoading = false;

  constructor(private backendService: BackendService) {}

  ngOnInit(): void {
    this.isLoading = true;
    this.backendService.getHistory().subscribe((data: any) => {
      this.jobHistory = data;
      this.isLoading = false;
    });
  }
}
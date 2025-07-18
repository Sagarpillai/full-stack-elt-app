import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router'; // Import this
import { BackendService } from '../../services/backend';

@Component({
  selector: 'app-data-viewer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './data-viewer.html',
  styleUrls: ['./data-viewer.css']
})
export class DataViewerComponent implements OnInit {
  tableData: any[] = [];
  headers: string[] = [];
  isLoading = false;
  tableName: string | null = null;

  constructor(
    private backendService: BackendService,
    private route: ActivatedRoute // Inject ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.isLoading = true;
    // Get the table name from the URL
    this.tableName = this.route.snapshot.paramMap.get('tableName');
    
    if (this.tableName) {
      this.backendService.getTableData(this.tableName).subscribe((data: any[]) => {
        this.tableData = data;
        if (data.length > 0) {
          this.headers = Object.keys(data[0]);
        }
        this.isLoading = false;
      });
    }
  }
}
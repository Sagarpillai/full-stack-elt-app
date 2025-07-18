import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  private apiUrl = 'http://127.0.0.1:5001';

  constructor(private http: HttpClient) { }

  getHistory(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/api/history`);
  }

  triggerJob(): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/api/trigger`, {});
  }

  // This is the updated function that your DataViewerComponent needs
  getTableData(tableName: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/api/table/${tableName}`);
  }
}
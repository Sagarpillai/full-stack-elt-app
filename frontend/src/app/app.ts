import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
// Import RouterModule here
import { RouterOutlet, RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  // And add RouterModule to the imports array
  imports: [CommonModule, RouterOutlet, RouterModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent {
  title = 'elt-frontend';
}
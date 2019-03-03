import { Component } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent {
  constructor(private http: HttpClient) {}
  title = "Tema1Front";
  text = "Welcome !";

  get_ip() {
    this.text = "Getting ip adress";
    this.http.get("http://localhost:8000/ip_addr").subscribe(response => {
      this.text = JSON.stringify(response, null, 2);
    });
  }

  get_details() {
    this.text = "Getting location details by ip_adress";
    this.http.get("http://localhost:8000/details").subscribe(response => {
      this.text = JSON.stringify(response, null, 2);
    });
  }

  get_time() {
    this.text = "Getting current date & time";
    this.http.get("http://localhost:8000/time").subscribe(response => {
      this.text = JSON.stringify(response, null, 2);
    });
  }

  get_places() {
    this.text = "Getting nearby places based on current time";
    this.http.get("http://localhost:8000/places").subscribe(response => {
      this.text = JSON.stringify(response, null, 2);
    });
  }
}

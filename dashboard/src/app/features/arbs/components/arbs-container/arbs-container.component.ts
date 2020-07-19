import { Component, OnInit } from '@angular/core';
import { ArbsStreamService } from '../../services/arbs-stream/arbs-stream.service';

@Component({
  selector: 'arbs-container',
  templateUrl: './arbs-container.component.html',
  styleUrls: ['./arbs-container.component.scss']
})
export class ArbsContainerComponent implements OnInit {

  constructor(private arbsStreamService: ArbsStreamService) { 
    this.arbsStreamService.onArbFound().subscribe((event) => console.log(event));
  }

  ngOnInit(): void {
  }

}

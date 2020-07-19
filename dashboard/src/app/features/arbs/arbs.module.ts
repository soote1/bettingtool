import { NgModule } from '@angular/core';

import { SharedModule } from './../../shared/shared.module';
import { ArbsRoutingModule } from './arbs-routing.module';
import { ArbsContainerComponent } from './components/arbs-container/arbs-container.component';
import { ArbsStreamService } from './services/arbs-stream/arbs-stream.service';
import { ArbsTableComponent } from './components/arbs-table/arbs-table/arbs-table.component';

@NgModule({
  declarations: [ArbsContainerComponent, ArbsTableComponent],
  imports: [
    SharedModule,
    ArbsRoutingModule
  ],
  providers:[
    ArbsStreamService
  ]
})
export class ArbsModule { }

import { NgModule } from '@angular/core';

import { SharedModule } from './../../shared/shared.module';
import { ArbsRoutingModule } from './arbs-routing.module';
import { ArbsContainerComponent } from './components/arbs-container/arbs-container.component';
import { ArbsStreamService } from './services/arbs-stream/arbs-stream.service';

@NgModule({
  declarations: [ArbsContainerComponent],
  imports: [
    SharedModule,
    ArbsRoutingModule
  ],
  providers:[
    ArbsStreamService
  ]
})
export class ArbsModule { }

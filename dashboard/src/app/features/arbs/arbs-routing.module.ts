import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ArbsContainerComponent } from './components/arbs-container/arbs-container.component';

const routes: Routes = [{ path: '', component: ArbsContainerComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ArbsRoutingModule { }

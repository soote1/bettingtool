import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [{ path: 'home', loadChildren: () => import('./features/home/home.module').then(m => m.HomeModule) }, { path: 'arbs', loadChildren: () => import('./features/arbs/arbs.module').then(m => m.ArbsModule) }];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

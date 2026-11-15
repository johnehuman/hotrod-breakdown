/* ---- odds engine: pure, testable ---- */
function makeRng(seed){let s=seed>>>0;return()=>{s=(s+0x6D2B79F5)>>>0;let t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296}}
function runSim(S,wk,N,forced){
  // wk: per team {live, proj} (ESPN live projection = finished + remaining); null = no live data
  const n=S.keys.length,r=makeRng(20261115);let spare=null;
  const g=()=>{if(spare!==null){const v=spare;spare=null;return v}let u=0,v=0;while(u===0)u=r();v=r();const m=Math.sqrt(-2*Math.log(u));spare=m*Math.sin(2*Math.PI*v);return m*Math.cos(2*Math.PI*v)};
  const po=new Float64Array(n),by=new Float64Array(n),top=new Float64Array(n);
  const G=S.sched[0].length,aw=new Float64Array(G),cond=[];for(let j=0;j<G;j++)cond.push({poA:[0,0,0,0],poH:[0,0,0,0]});
  const m=new Float64Array(n),w=new Float64Array(n),pf=new Float64Array(n),sc=new Float64Array(n),idx=[...Array(n).keys()];
  const res=new Uint8Array(G);
  for(let it=0;it<N;it++){
    for(let i=0;i<n;i++){m[i]=S.mu[i]+g()*S.tsd;w[i]=S.W[i];pf[i]=S.PF[i]}
    for(let wi=0;wi<S.sched.length;wi++){
      for(let i=0;i<n;i++){
        if(wi===0&&wk){const rem=Math.max(0,wk[i].proj-wk[i].live);sc[i]=wk[i].live+rem+(rem>0?g()*S.sd*Math.sqrt(Math.min(1,rem/S.mu[i])):0)}
        else sc[i]=m[i]+g()*S.sd;
      }
      if(wi===0&&forced)S.sched[0].forEach(([a,h],j)=>{const f=forced[j];if((f==='a'&&sc[a]<=sc[h])||(f==='h'&&sc[h]<=sc[a])){const t=sc[a];sc[a]=sc[h];sc[h]=t;if(sc[a]===sc[h])sc[f==='a'?a:h]+=0.01}});
      for(let i=0;i<n;i++)pf[i]+=sc[i];
      S.sched[wi].forEach(([a,h],j)=>{const x=sc[a]>sc[h];w[x?a:h]++;if(wi===0)res[j]=x?1:0});
    }
    idx.sort((a,b)=>(w[b]-w[a])||(pf[b]-pf[a]));
    const seed=new Int32Array(n);idx.forEach((t,s)=>seed[t]=s);
    for(let i=0;i<n;i++){if(seed[i]<6)po[i]++;if(seed[i]<2)by[i]++;if(seed[i]===0)top[i]++}
    for(let j=0;j<G;j++){const [a,h]=S.sched[0][j],c=cond[j],k=res[j]?0:2;aw[j]+=res[j];
      c.poA[k]+=seed[a]<6;c.poA[k+1]+=seed[a]<2;c.poH[k]+=seed[h]<6;c.poH[k+1]+=seed[h]<2}
  }
  const pc=x=>x/N*100;
  return{po:[...po].map(pc),by:[...by].map(pc),top:[...top].map(pc),games:S.sched[0].map(([a,h],j)=>{const c=cond[j],na=aw[j],nh=N-aw[j],d=(x,k)=>k?x/k*100:null;
    return{a,h,pa:na/N*100,
      a_win:[d(c.poA[0],na),d(c.poA[1],na)],a_loss:[d(c.poA[2],nh),d(c.poA[3],nh)],
      h_win:[d(c.poH[2],nh),d(c.poH[3],nh)],h_loss:[d(c.poH[0],na),d(c.poH[1],na)]}})};
}
function parseMatchups(S,payload){
  const wk=S.keys.map(()=>null);let at=null,allFinal=true;
  for(const mu of (payload&&payload.matchups)||[]){
    at=at||(mu.scoring&&mu.scoring.fetchedAt);if(!mu.final)allFinal=false;
    for(const side of ['away','home']){const t=mu[side];if(!t)continue;const k=S.byName[String(t.teamName).trim()];if(k==null)continue;
      const live=+t.livePoints||0,proj=t.projectedPoints==null?live:+t.projectedPoints;wk[k]={live,proj:Math.max(live,proj)}}
  }
  return{wk:wk.every(Boolean)?wk:null,at,allFinal};
}
if(typeof module!=='undefined')module.exports={runSim,parseMatchups};

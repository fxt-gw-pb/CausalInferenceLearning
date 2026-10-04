export const STORAGE_KEY='causal-study:v1';
export const freshState=()=>({version:1,bookmarks:[],completed:[],answers:{},lastLesson:null});
export function validateState(raw,validIds){
  const ids=new Set(validIds), value=raw&&typeof raw==='object'?raw:{};
  const unique=(xs)=>[...new Set(Array.isArray(xs)?xs.filter(x=>typeof x==='string'&&ids.has(x)):[])];
  const answers={};
  if(value.answers && typeof value.answers==='object'&&!Array.isArray(value.answers)){
    for(const [key,v] of Object.entries(value.answers)) if(/^[a-z0-9-]{1,100}$/.test(key)&&Number.isInteger(v)&&v>=0&&v<5) answers[key]=v;
  }
  return {version:1,bookmarks:unique(value.bookmarks),completed:unique(value.completed),answers,lastLesson:ids.has(value.lastLesson)?value.lastLesson:null};
}
export function loadState(storage,validIds){
  try {return {state:validateState(JSON.parse(storage.getItem(STORAGE_KEY)||'null'),validIds),persisted:true};}
  catch {return {state:freshState(),persisted:false};}
}
export function saveState(storage,state){try{storage.setItem(STORAGE_KEY,JSON.stringify(state));return true;}catch{return false;}}
export function toggleId(list,id){return list.includes(id)?list.filter(x=>x!==id):[...list,id];}
export function searchLessons(lessons,query){
  const terms=query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  if(!terms.length)return [];
  return lessons.filter(l=>{const t=[l.title,l.summary,...l.tags,...l.sections.map(s=>s.title),...l.sections.flatMap(s=>s.blocks.filter(b=>b.type==='paragraph').map(b=>b.text))].join(' ').toLocaleLowerCase();return terms.every(q=>t.includes(q));});
}

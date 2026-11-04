(function(root){
function valid(value){if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(value))return false;const date=new Date(value+'T12:00:00Z');return Number.isFinite(date.getTime())&&date.toISOString().slice(0,10)===value;}
function today(now=new Date()){return new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Istanbul'}).format(now);}
function add(value,days){if(!valid(value)||!Number.isInteger(Number(days))||Number(days)<0||Number(days)>36500)return '';const d=new Date(value+'T12:00:00Z');d.setUTCDate(d.getUTCDate()+Number(days));return d.toISOString().slice(0,10);}
function quoteDate(p){if(valid(p.quoteDate))return p.quoteDate;if(p.created&&Number.isFinite(Date.parse(p.created)))return today(new Date(p.created));return '';}
function validUntil(p){const days=p.terms?.validityDays;return days!==''&&days!=null?add(quoteDate(p),days):'';}
function classify(p,asOf=today()){const active=!['sent','cancelled'].includes(p.status),due=valid(p.responseDue)?p.responseDue:'',end=validUntil(p);return {overdue:!!(active&&due&&due<asOf),upcoming:!!(active&&due&&due>=asOf&&due<=add(asOf,3)),expired:!!(p.status!=='cancelled'&&end&&end<asOf),validUntil:end};}
function format(value){return valid(value)?value.split('-').reverse().join('.'): '—';}
root.QuoteDates={valid,today,add,quoteDate,validUntil,classify,format};
})(globalThis);

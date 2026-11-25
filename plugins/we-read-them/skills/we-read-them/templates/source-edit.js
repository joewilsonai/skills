// Optional companion for the portrait reel, intro and widescreen pages. Copy beside index.html.
// Define window.WRT_SOURCE_EDIT before the template's main script. Both canvas sizes take the same edit.
// For presentation:'quiet', copy aibc-brand/ next to this file. The Club's source credit and
// captions stay readable while the rank appears briefly at chapter entry.
// {rank:2, title:'A call home', assets:{cup:{image:'assets/cup.jpg'}, game:{frames:60,dir:'assets/game'}},
//  scenes:[{at:0,layout:'archive',asset:'game',credit:'NFL Films · 2000'},
//          {at:{take:2},layout:'compare',asset:'cup',credit:'AP · 2000',heading:'Super Bowl XXXIV',note:'St. Louis 23 · Tennessee 16'}]}
// audioEnd may be the probed approved mix duration in seconds. Otherwise preserve the standard
// takes.dur + .8 mix tail. endCard:false creates an excerpt; endCard:'source' holds the credited final image. Copy
// window.WRT_CHAPTER_META (with an episode slug) into wide/meta.json for the normal long-form cut.
// Frame sources are 001.jpg ... NNN.jpg in dir at asset.fps (default 30). Cues accept seconds,
// {take, offset} or {take, word, occurrence, offset}; occurrence counts from one.
// Optional take.display_words entries are [printed token, first spoken onset, last spoken end].
// “contain” preserves the complete image outside the label/caption regions. With fit:'cover', inspect
// both crops, especially scorebugs and faces. focus:[x,y] and crop:[x,y,w,h] use source fractions.
// portrait:{fit,focus,crop,asset} or wide:{fit,focus,crop,asset} can use checked native crops
// or a separately prepared excerpt of the same source. Its attribution must stay accurate.

const clamp = (value, low, high) => Math.max(low, Math.min(value, high));

async function loadClubBrand() {
  const directory=new URL('./aibc-brand/',import.meta.url);
  const response=await fetch(new URL('brand.json',directory));
  if (!response.ok) throw new Error('The quiet presentation needs aibc-brand/ beside source-edit.js');
  const brand=await response.json();
  const faces=await Promise.all(Object.values(brand.fonts).map(font=>{
    const source=new URL(font.file,directory);
    return new FontFace(font.family,`url("${source.href}")`,{weight:font.weightRange??String(font.weight)}).load();
  }));
  faces.forEach(face=>document.fonts.add(face));
  return brand;
}

async function loadImage(url) {
  const image = new Image();
  image.src = url;
  try { await image.decode(); }
  catch { throw new Error(`Could not load the source image ${url}`); }
  return image;
}

async function loadAsset(asset) {
  if (asset.image) return [await loadImage(asset.image)];
  if (!asset.dir || !Number.isInteger(asset.frames) || asset.frames < 1 || !(Number(asset.fps ?? 30) > 0)) {
    throw new Error('A sequence needs dir, a positive frame count and a positive frame rate');
  }
  return Promise.all(Array.from({length:asset.frames}, (_, i) =>
    loadImage(`${asset.dir}/${String(i+1).padStart(3, '0')}.jpg`)));
}

function cueTime(at, takes) {
  if (typeof at === 'number') return at;
  const take = at && Number.isInteger(at.take) && takes[at.take];
  if (!take || !Number.isFinite(at.offset ?? 0)) throw new Error('A picture cue needs seconds or a valid take and offset');
  let start = take.t0;
  if (at.word !== undefined) {
    const key = word => String(word).normalize('NFC').toLowerCase().replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, '');
    const occurrence = at.occurrence ?? 1;
    const matches = (take.words || []).filter(([word]) => key(word) === key(at.word));
    if (!key(at.word) || !Number.isInteger(occurrence) || occurrence < 1 || !matches[occurrence - 1]) {
      throw new Error(`No timed occurrence ${occurrence} of "${at.word}" in take ${at.take}`);
    }
    start = matches[occurrence - 1][1];
  }
  return start + (at.offset ?? 0);
}

// Split from the timed script. Never truncate a third wrapped line or drop a word to fit an overlay.
function buildCaptions(takes, measure, limit, style) {
  const cues=[];
  for (const take of takes) {
    const tokens=take.text.trim().split(/\s+/).filter(Boolean), words=take.words || [];
    const displayWords=take.display_words;
    if (displayWords !== undefined) {
      if (!Array.isArray(displayWords) || displayWords.length !== tokens.length) {
        throw new Error('display_words needs one timed entry per printed token');
      }
      for (const [i, span] of displayWords.entries()) {
        if (!Array.isArray(span) || span[0] !== tokens[i] || !Number.isFinite(span[1]) ||
            !Number.isFinite(span[2]) || span[2] < span[1] || span[1] < take.t0 || span[2] > take.t1 ||
            (i > 0 && span[1] < displayWords[i-1][1])) {
          throw new Error(`Invalid display_words span for printed token ${i+1} ("${tokens[i]}")`);
        }
      }
    }
    function start(i) {
      if (displayWords) return displayWords[i][1];
      if (words.length) return words[Math.round(i*(words.length-1)/Math.max(1,tokens.length-1))][1];
      return take.t0+(take.t1-take.t0)*i/tokens.length;
    }
    let first=0,line='',lineCount=1,phrase=[];
    for (let i=0;i<tokens.length;i++) {
      const token=tokens[i],candidate=line ? `${line} ${token}` : token;
      if (line && measure(candidate,style)>limit) {
        if (lineCount===2) {
          cues.push([start(first),start(i),phrase.join(' '),take.who]);first=i;phrase=[];lineCount=1;
        } else lineCount++;
        line=token;
      } else line=candidate;
      phrase.push(token);
      if (i===tokens.length-1 || (/[.!?][”'’"]?$/.test(token) && phrase.length>=3)) {
        cues.push([start(first),i===tokens.length-1 ? take.t1+.18 : start(i+1),phrase.join(' '),take.who]);
        first=i+1;phrase=[];line='';lineCount=1;
      }
    }
  }
  for (let i=0;i+1<cues.length;i++) cues[i][1]=Math.min(cues[i][1],cues[i+1][0]);
  return cues;
}

function cropOf(scene) {
  const [x,y,w,h]=scene.crop || [0,0,1,1];
  if (![x,y,w,h].every(Number.isFinite) || x<0 || y<0 || w<=0 || h<=0 || x+w>1.000001 || y+h>1.000001) {
    throw new Error(`Invalid source crop for ${scene.asset}`);
  }
  return [x,y,w,h];
}

function insideCrop(inner, outer) {
  return inner[0] >= outer[0] - .000001 && inner[1] >= outer[1] - .000001 &&
    inner[0] + inner[2] <= outer[0] + outer[2] + .000001 &&
    inner[1] + inner[3] <= outer[1] + outer[3] + .000001;
}

// Each overlay owns a measured rectangle. Shrink only if the whole phrase cannot fit at the design size.
function drawBlock(drawText, measure, value, [left,top,width,height], options) {
  if (!value) return;
  for (let size=options.size;size>=Math.round(options.size*.6);size--) {
    const style={s:size,w:options.weight??700,f:options.font??'Sans',c:options.color??'#faf8f1'};
    const lines=[];
    for (const token of value.trim().split(/\s+/)) {
      const i=lines.length-1;
      if (i>=0 && measure(`${lines[i]} ${token}`,style)<=width) lines[i]+=` ${token}`;
      else lines.push(token);
    }
    if (options.id==='caption' && lines.length===2) {
      const words=value.trim().split(/\s+/);let best=Infinity;
      for (let split=1;split<words.length;split++) {
        const a=words.slice(0,split).join(' '), b=words.slice(split).join(' ');
        const wA=measure(a,style), wB=measure(b,style);
        const orphan=options.avoidOrphans && words.length>=4 && (split===1 || split===words.length-1);
        const diff=Math.abs(wA-wB)+(orphan ? width*2 : 0);
        if (Math.max(wA,wB)<=width && diff<best) {lines[0]=a;lines[1]=b;best=diff;}
      }
    }
    const leading=size*1.24,blockHeight=size+(lines.length-1)*leading;
    if (blockHeight>height || lines.some(line=>measure(line,style)>width)) continue;
    const first=top+size*.84+(options.bottom ? height-blockHeight : 0);
    lines.forEach((line,i)=>drawText(line,left,first+leading*i,{...style,id:`${options.id}-${i}`}));
    return;
  }
  throw new Error(`Text exceeds its safe area (${options.id}): ${value}`);
}

function drawMedia(ctx,image,box,crop,cover,focus,zoom) {
  const [x,y,w,h]=box,[u,v,cw,ch]=crop;
  const sourceW=image.width*cw,sourceH=image.height*ch;
  const scale=(cover ? Math.max : Math.min)(w/sourceW,h/sourceH)*zoom;
  const dw=sourceW*scale,dh=sourceH*scale;
  // focus is measured on the complete source. Translate into the crop before fitting the output.
  const fx=focus ? clamp((focus[0]-u)/cw,0,1) : .5;
  const fy=focus ? clamp((focus[1]-v)/ch,0,1) : .5;
  const px=dw>w ? x+clamp(w/2-fx*dw,w-dw,0) : x+(w-dw)/2;
  const py=dh>h ? y+clamp(h/2-fy*dh,h-dh,0) : y+(h-dh)/2;
  ctx.save();ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();
  ctx.drawImage(image,u*image.width,v*image.height,sourceW,sourceH,px,py,dw,dh);
  ctx.restore();
  return ([rx,ry,rw,rh]) => [px+(rx-u)*dw/cw,py+(ry-v)*dh/ch,rw*dw/cw,rh*dh/ch];
}

function outline(ctx, box, color, weight) {
  const [x,y,w,h] = box;
  ctx.lineJoin = 'round';
  ctx.strokeStyle = 'rgba(10,18,21,.82)';
  ctx.lineWidth = weight + 3;
  ctx.strokeRect(x,y,w,h);
  ctx.strokeStyle = color;
  ctx.lineWidth = weight;
  ctx.strokeRect(x,y,w,h);
}

// First establish the whole source. Outline the detail on its own pixels, then move the
// context aside while a second, undistorted view of those same pixels opens beside/below it.
function drawReveal(ctx, image, scene, t, wide, accent) {
  const whole = wide ? [80,154,1760,636] : [52,304,874,992];
  const context = wide ? [72,230,526,496] : [62,301,856,320];
  const close = wide ? [638,151,1206,648] : [60,659,862,621];
  const elapsed = t - scene.detail.start;
  const travel = clamp((elapsed - .36) / .37, 0, 1);
  const eased = travel*travel*(3-2*travel);
  const box = whole.map((value,i) => value+(context[i]-value)*eased);
  const locate = drawMedia(ctx,image,box,scene.crop,false,null,1);
  if (elapsed < 0) return;
  ctx.save();
  ctx.globalAlpha = clamp(elapsed/.12,0,1);
  outline(ctx,locate(scene.detail.crop),accent,wide?4:5);
  ctx.restore();
  if (!travel) return;
  ctx.save();
  ctx.globalAlpha = eased;
  const locateDetail = drawMedia(ctx,image,close,scene.detail.crop,false,null,1);
  if (scene.detail.mark) {
    // A short underline locates the line without painting over the original letters.
    const [x,y,w,h] = locateDetail(scene.detail.mark);
    ctx.strokeStyle = 'rgba(10,18,21,.75)';
    ctx.lineWidth = 7;
    ctx.beginPath();ctx.moveTo(x,y+h);ctx.lineTo(x+w,y+h);ctx.stroke();
    ctx.strokeStyle = accent;ctx.lineWidth = 4;ctx.stroke();
  }
  ctx.restore();
}

export async function prepareSourceEdit({canvas,takes,config,drawText,measure}) {
  const ctx=canvas.getContext('2d'),W=canvas.width,H=canvas.height,wide=W>H;
  const bar=(x,y,w,h,color)=>{ctx.fillStyle=color;ctx.fillRect(x,y,w,h);};
  const quiet=config.presentation==='quiet';
  if (!config.scenes?.length || !config.assets) throw new Error('Source edit needs scenes and assets');
  const scenes=config.scenes.map(scene=>{
    const view=scene[wide?'wide':'portrait'] || {};
    const framed={...scene,asset:view.asset??scene.asset,fit:view.fit??scene.fit,focus:view.focus??scene.focus,crop:view.crop??scene.crop};
    framed.start=cueTime(scene.at,takes.takes);
    framed.crop=cropOf(framed);
    if (scene.layout==='reveal') {
      const detail={...scene.detail,...view.detail};
      if (!detail.crop) throw new Error(`A reveal needs a detail crop for ${framed.asset}`);
      framed.detail={start:cueTime(detail.at,takes.takes),crop:cropOf({asset:framed.asset,crop:detail.crop})};
      if (detail.mark) framed.detail.mark=cropOf({asset:framed.asset,crop:detail.mark});
      if (!insideCrop(framed.detail.crop,framed.crop) ||
          (framed.detail.mark && !insideCrop(framed.detail.mark,framed.detail.crop))) {
        throw new Error(`The detail must be visible in its context and the mark inside the detail: ${framed.asset}`);
      }
    }
    return framed;
  });
  scenes.forEach((scene,i)=>{
    if (!Number.isFinite(scene.start) || (i===0 ? scene.start!==0 : scene.start<=scenes[i-1].start) || scene.start>takes.dur) throw new Error('Scene starts must ascend from zero within the mix');
    if (!['archive','document','compare','immersive','reveal'].includes(scene.layout) || !config.assets[scene.asset] || !scene.credit) throw new Error(`Scene ${i+1} needs a valid layout, source asset and credit`);
    if (scene.layout==='compare' && !scene.heading) throw new Error(`Comparison scene ${i+1} needs a heading`);
    if (scene.layout==='reveal' && (!(scene.detail.start>=scene.start) ||
        scene.detail.start >= (scenes[i+1]?.start ?? takes.dur))) throw new Error(`The reveal cue must fall inside scene ${i+1}`);
    if (scene.fit && !['contain','cover'].includes(scene.fit)) throw new Error(`Invalid fit on scene ${i+1}`);
    if ((scene.focus && (scene.focus.length!==2 || !scene.focus.every(v=>Number.isFinite(v)&&v>=0&&v<=1))) || (scene.push && (!Number.isFinite(scene.push)||scene.push<1||scene.push>1.12))) throw new Error(`Invalid focus or push on scene ${i+1}`);
  });
  const brand=quiet?await loadClubBrand():null;
  if (!brand) await Promise.all(['700 40px Sans','400 24px Sans','600 24px Mono'].map(font=>document.fonts.load(font)));
  const ink=brand?.colors.ink??(config.background||'#111b20');
  const accent=brand?.colors.accentOnInk??(config.accent||'#fac366');
  const styles={};
  if (brand) {
    const {display,label,body}=brand.fonts,{cream,muted}=brand.colors;
    const style=(face,color,weight=face.weight)=>({font:face.family,weight,color});
    styles.credit=style(label,cream);
    styles.rank=style(display,accent);
    styles.comparison=style(display,cream);
    styles['comparison-note']=style(body,muted);
    styles['voice-source']=style(label,accent);
    styles.caption=style(body,cream,body.captionWeight);
    styles.endcard=styles.comparison;
    styles['endcard-chapter']=style(body,cream);
  }
  const text=(value,box,opts)=>drawBlock(drawText,measure,value,box,{...opts,...styles[opts.id]});
  const media=Object.fromEntries(await Promise.all([...new Set(scenes.map(s=>s.asset))].map(async key=>[key,await loadAsset(config.assets[key])])));
  const left=wide?76:64,captionBox=wide?[left,873,1570,128]:[left,1415,810,189];
  const captionSize=wide?60:66,creditSize=wide?27:31;
  const cues=buildCaptions(takes.takes,measure,captionBox[2],
    {s:captionSize,w:styles.caption?.weight??700,f:styles.caption?.font??'Sans'});
  const rank=config.rank===0 ? 'INTRO' : config.rank==null ? '' : `#${config.rank}`;
  const audioEnd=config.audioEnd ?? takes.dur+.8;
  if (!Number.isFinite(audioEnd) || audioEnd<0) throw new Error('audioEnd must be a measured duration in seconds');
  const lastSpeechEnd=Math.max(takes.dur,...takes.takes.map(cue=>cue.t1),...takes.takes.flatMap(cue=>(cue.words||[]).map(word=>word[2]??0)));
  // Never cut inside known speech. The standard mixer allocates .8 s beyond the timing manifest.
  const endcardAt=Math.ceil(Math.max(lastSpeechEnd,audioEnd)*30)/30;
  const hasEndCard=config.endCard!==false;
  const duration=endcardAt+(hasEndCard ? 1.6 : 0);
  const meta={chapter:rank ? `${rank==='INTRO'?'Intro':rank} · ${config.title}` : config.title,endcard_at:endcardAt};
  if (config.slug) meta.slug=config.slug;
  function render(t) {
    const sourceEnding=config.endCard==='source' && t>=endcardAt;
    const sourceTime=sourceEnding ? Math.max(0,endcardAt-1/30) : t;
    const index=scenes.findLastIndex(scene=>sourceTime>=scene.start),s=scenes[Math.max(0,index)],list=media[s.asset];
    const duration=(scenes[index+1]?.start ?? takes.dur)-s.start,progress=clamp((sourceTime-s.start)/Math.max(.01,duration),0,1);
    const frame=clamp(Math.floor((sourceTime-s.start)*(config.assets[s.asset].fps??30)),0,list.length-1);
    const sourceFirst=s.layout==='immersive';
    const cover=s.fit==='cover',immersive=sourceFirst || (cover && s.layout==='archive');
    bar(0,0,W,H,ink);
    let box=wide?[0,140,W,690]:[0,268,W,1030];
    if (immersive) box=[0,0,W,H];
    if (sourceFirst && !cover) box=wide?[40,142,W-80,665]:[42,264,888,1034];
    if (s.layout==='compare') box=wide?[705,180,1139,612]:[64,514,952,720];
    if (s.layout==='document') {
      const paper=wide?[118,175,1684,620]:[48,355,984,794];
      bar(...paper,brand?.colors.paper??'#f2f0e7');
      const inset=wide?68:31;
      box=[paper[0]+inset,paper[1]+inset,paper[2]-inset*2,paper[3]-inset*2];
    }
    // Documentary pages stay still. A photograph can ease up to 12% toward a checked focal point.
    const zoom=list.length===1 && (s.layout==='archive' || sourceFirst) && cover ? 1+((s.push??1)-1)*progress : 1;
    if (s.layout==='reveal') drawReveal(ctx,list[frame],s,sourceTime,wide,accent);
    else drawMedia(ctx,list[frame],box,s.crop,s.layout!=='document' && cover,s.focus,zoom);
    if (immersive) {
      const scrim=brand?.colors.ink??'#060b0f';
      const top=ctx.createLinearGradient(0,0,0,wide?290:425);top.addColorStop(0,brand?scrim+'e6':'rgba(6,11,15,.9)');top.addColorStop(1,scrim+'00');bar(0,0,W,wide?290:425,top);
      const bottom=ctx.createLinearGradient(0,wide?690:1110,0,wide?1030:1660);bottom.addColorStop(0,scrim+'00');bottom.addColorStop(1,brand?scrim+'f0':'rgba(6,11,15,.94)');bar(0,wide?690:1110,W,H,bottom);
    }
    if (hasEndCard && t>=endcardAt && !sourceEnding) {
      bar(0,0,W,H,ink);
      const ax=wide?126:76,ay=wide?360:655;
      bar(ax,ay,wide?84:72,8,brand?.colors.stamp??accent);
      text('WE READ THEM',[ax,ay+46,W-ax*2,wide?165:210],{size:wide?122:100,id:'endcard'});
      text(config.title,[ax,ay+(wide?217:261),W-ax*2,wide?161:220],{size:wide?45:49,weight:400,color:'#ced5d5',id:'endcard-chapter'});
      return;
    }
    if (quiet || sourceFirst) {
      const creditWidth=wide?1510:(quiet?692:816);
      text(s.credit,[left,wide?48:91,creditWidth,wide?81:106],
        {size:quiet?(wide?44:38):creditSize,font:'Mono',weight:600,color:'#faf7ee',id:'credit'});
      if (quiet && config.rank>0 && t<2.5 && !sourceEnding) {
        text(rank,wide?[1640,48,200,81]:[792,91,130,106],
          {size:wide?44:38,font:'Mono',weight:600,color:accent,id:'rank'});
      }
      if (sourceEnding && !quiet) text('WE READ THEM',[left,wide?899:1473,wide?660:810,wide?77:80],
        {size:wide?32:38,font:'Mono',weight:600,color:accent,id:'source-end'});
    } else {
      text('WE READ THEM',[left,wide?17:52,wide?500:790,wide?28:41],{size:wide?21:28,font:'Mono',weight:600,color:accent,id:'series'});
      const top=wide?51:102,rankW=rank ? measure(rank,{s:wide?42:48,f:'Mono',w:600})+32 : 0;
      if (rank) {
        bar(left,top,rankW,wide?65:75,accent);
        text(rank,[left+16,top+(wide?10:12),rankW-31,60],{size:wide?42:48,font:'Mono',weight:600,color:'#10171b',id:'rank'});
      }
      const creditBox=wide?[1200,top+8,644,81]:[left,top+99,832,107];
      const titleStart=left+rankW+(rank?22:0),titleEnd=wide ? creditBox[0]-36 : 914;
      text(config.title,[titleStart,top+(wide?12:16),titleEnd-titleStart,wide?65:81],{size:wide?39:41,id:'chapter'});
      text(s.credit,creditBox,{size:creditSize,font:'Mono',weight:600,color:'#f6f0df',id:'credit'});
    }
    if (s.layout==='compare') {
      const heading=wide?[left,294,570,233]:[left,318,840,124];
      text(s.heading,heading,{size:wide?76:60,id:'comparison'});
      const note=wide?[left,548,570,174]:[left,450,850,58];
      const noteSize=quiet?(wide?44:38):(wide?35:33);
      text(s.note,note,{size:noteSize,weight:400,color:'#ced5d5',id:'comparison-note'});
    }
    if (sourceEnding) return;
    const cue=cues.find(([from,to])=>t>=from && t<to);
    if (!cue) return;
    const [, ,line,who]=cue;
    const role=who==='C' ? (s.speaker ? `${s.speaker} · original audio` : 'Original audio')
      : who==='R' || who===true ? (s.reader ? `${s.reader} · read from the record` : 'Read from the record') : '';
    if (role) {
      const roleBox=wide?[left,quiet?823:829,1590,quiet?47:38]:[left,1330,810,78];
      const roleSize=quiet?(wide?44:38):(wide?26:30);
      text(role,roleBox,{size:roleSize,font:'Mono',weight:600,color:accent,id:'voice-source'});
    }
    text(line,captionBox,{size:captionSize,id:'caption',avoidOrphans:!wide});
  }
  return {render,duration,meta};
}

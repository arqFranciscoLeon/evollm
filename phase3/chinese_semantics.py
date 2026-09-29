"""Prose-derived Chinese reference rules; no imports or calls to archived code."""
class Reference:
    def __init__(self,profile):
        self.profile=profile; self.started=False; self.permanent=False; self.cooldown=False; self.used=False

    def step(self,mine,opp):
        p=self.profile; n=len(opp); r=n+1
        if p=='always_d': return 'D'
        if p.startswith(('tft_','wsls_','dd_')) and p!='dd_latch_1000':
            family,start,end=p.split('_')
            if not n: return start
            if end!='none' and r>=int(end): return 'D'
            if family=='tft': return opp[-1]
            if family=='wsls': return 'C' if mine[-1]==opp[-1] else 'D'
            return 'C' if mine[-1]==opp[-1]=='D' else 'D'
        if p in ('anti','anti991'):
            return 'D' if not n or p=='anti991' and r>=991 or opp[-1]=='C' else 'C'
        if p=='grim_D': return 'D' if not n or 'D' in opp else 'C'
        if p=='twoC_elseD': return 'C' if n>=2 and opp[-2:]=='CC' else 'D'
        if p in ('twoD','twoD_second_tft'):
            if p=='twoD_second_tft' and n==1: return opp[-1]
            return 'D' if n>=2 and opp[-2:]=='DD' else 'C'
        if p=='forgiving_DD': return 'D' if n and mine[-1]=='C' and opp[-1]=='D' else 'C'
        if p=='ratio15_DD10':
            return 'D' if n and (opp[-1]=='D' or 100*opp.count('D')>15*n or n>=10 and 'DD' in opp[-10:]) else 'C'
        if p in ('trust3_991','trust5'):
            if p=='trust3_991' and r>=991: return 'D'
            if self.permanent: return 'D'
            if self.started:
                if opp[-1]=='D': self.permanent=True; return 'D'
                return 'C'
            k=3 if p=='trust3_991' else 5
            if n>=k and opp[-k:]=='C'*k and (k==3 or mine[-k:]=='D'*k):
                self.started=True; return 'C'
            return 'D'
        if p=='switch100':
            if n>=100 and mine[-100:]=='D'*100 and opp[-100:]=='C'*100: self.started=True
            return 'C' if self.started else 'D'
        if p=='probe10_once':
            if not self.used and n>=10 and mine[-10:]=='D'*10 and opp[-10:]=='C'*10:
                self.used=True; return 'C'
            return 'D'
        if p=='dd_latch_1000':
            if n and mine[-1]=='C' and opp[-1]=='D': self.permanent=True
            return 'D' if self.permanent or r==1000 or not n or mine[-1]!=opp[-1] or opp[-1]=='C' else 'C'
        if p=='keepCC_elseD': return 'C' if n and mine[-1]==opp[-1]=='C' else 'D'
        if p=='probeDC2': return 'C' if n>=2 and mine[-2:]=='DD' and opp[-2:]=='CC' else 'D'
        if p=='baitDDD':
            if self.cooldown: self.cooldown=False; return 'D'
            if n>=3 and opp[-3:]=='DDD': self.cooldown=True; return 'C'
            return 'D'
        if p=='afterDDD': return 'C' if n>=3 and opp[-3:]=='DDD' else 'D'
        if p=='probeDC_lock':
            if n==0: return 'D'
            if n==1: return 'C'
            return 'D' if opp[:2]=='CC' else opp[-1]
        if p=='afterDD10': return 'C' if n>=10 and mine[-10:]==opp[-10:]=='D'*10 else 'D'
        if p in ('probeDD_CC','probeDD_C'):
            if n<2 or opp[:2]=='CC': return 'D'
            if n< (4 if p=='probeDD_CC' else 3): return 'C'
            return opp[-1]
        if p=='DD2_unlessD5':
            return 'D' if n>=5 and opp[-5:]=='DDDDD' else ('C' if n>=2 and mine[-2:]==opp[-2:]=='DD' else 'D')
        if p=='treeCDC':
            if n<2 or opp[0]=='D' or opp[1]=='C' or r==1000: return 'D'
            if n==2: return 'C'
            return 'D' if opp[2]=='D' else 'C'
        if p=='firstD_twoC':
            if r==1000 or 'D' not in opp: return 'D'
            delta=n-1-opp.index('D')
            return 'C' if delta<2 else opp[-1]
        if p=='probeDCC':
            if n==0 or r==1000: return 'D'
            if n<3: return 'C'
            return 'D' if opp[1:3]=='CC' else opp[-1]
        if p=='ownD5': return 'C' if n>=5 and mine[-5:]=='DDDDD' and opp[-1]=='D' else 'D'
        raise ValueError('Unadjudicated or unknown profile '+p)

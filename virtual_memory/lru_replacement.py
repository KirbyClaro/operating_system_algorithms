"""LRU Page Replacement — Least Recently Used."""
import tkinter as tk
from tkinter import messagebox
from collections import OrderedDict

BG="#F7F8FA";SURFACE="#FFFFFF";BORDER="#E2E5EB";TEXT_PRI="#0D0F14";TEXT_SEC="#6B7280"
HIT_BG="#ECFDF5";HIT_FG="#059669";FAULT_BG="#FEF2F2";FAULT_FG="#DC2626";EMPTY_FG="#CBD5E1"
BTN_FG="#FFFFFF";ACCENT="#0891B2";ACCENT_L="#ECFEFF";FONT="Segoe UI"

def run_algorithm(pages,capacity):
    cache=OrderedDict(); faults=hits=0; log=[]
    for page in pages:
        if page in cache:
            cache.move_to_end(page); hits+=1; status="HIT"; extra=f"Page {page} moved to MRU position"
        else:
            faults+=1; status="FAULT"; extra=""
            if len(cache)==capacity:
                evicted,_=cache.popitem(last=False); extra=f"Evicted page {evicted} (least recently used)"
            cache[page]=True
        log.append({"page":page,"frames":list(cache.keys()),"status":status,"extra":extra})
    return faults,hits,log

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("LRU Page Replacement"); self.configure(bg=BG)
        self.geometry("860x660"); self._log=[]; self._step=-1; self._capacity=3; self._build_ui()

    def _build_ui(self):
        bar=tk.Frame(self,bg=ACCENT,pady=16); bar.pack(fill="x")
        tk.Label(bar,text="LRU  ·  Page Replacement",font=(FONT,18,"bold"),bg=ACCENT,fg=BTN_FG).pack()
        tk.Label(bar,text="Least Recently Used  —  evicts the page not accessed for the longest time",font=(FONT,9),bg=ACCENT,fg="#a5f3fc").pack()
        row=tk.Frame(self,bg=BG,padx=20,pady=12); row.pack(fill="x")
        lf=tk.Frame(row,bg=SURFACE,highlightthickness=1,highlightbackground=BORDER)
        lf.pack(side="left",fill="x",expand=True,ipady=4,ipadx=8)
        tk.Label(lf,text="Reference String",font=(FONT,8),bg=SURFACE,fg=TEXT_SEC).pack(anchor="w",padx=6,pady=(4,0))
        self.ref_var=tk.StringVar(value="7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1")
        tk.Entry(lf,textvariable=self.ref_var,font=("Consolas",11),bg=SURFACE,fg=TEXT_PRI,insertbackground=TEXT_PRI,relief="flat",bd=0).pack(fill="x",padx=6,pady=(0,4))
        rf=tk.Frame(row,bg=SURFACE,highlightthickness=1,highlightbackground=BORDER)
        rf.pack(side="left",padx=(10,0),ipady=4,ipadx=8)
        tk.Label(rf,text="Frames",font=(FONT,8),bg=SURFACE,fg=TEXT_SEC).pack(anchor="w",padx=6,pady=(4,0))
        self.cap_var=tk.IntVar(value=3)
        tk.Spinbox(rf,from_=1,to=10,textvariable=self.cap_var,width=4,font=("Consolas",12),bg=SURFACE,fg=TEXT_PRI,relief="flat",bd=0,buttonbackground=BG).pack(padx=6,pady=(0,4))
        tk.Button(row,text="  Start  ",command=self._on_start,font=(FONT,10,"bold"),bg=ACCENT,fg=BTN_FG,relief="flat",bd=0,padx=14,pady=8,cursor="hand2").pack(side="left",padx=(10,0))
        outer=tk.Frame(self,bg=BG,padx=20); outer.pack(fill="x")
        tk.Label(outer,text="MEMORY FRAMES",font=(FONT,8,"bold"),bg=BG,fg=TEXT_SEC).pack(anchor="w",pady=(4,6))
        self._cells_frame=tk.Frame(outer,bg=BG); self._cells_frame.pack(anchor="w"); self._cells=[]
        sbar=tk.Frame(self,bg=BG,padx=20,pady=6); sbar.pack(fill="x")
        self._lbl_page=tk.Label(sbar,text="",font=(FONT,13,"bold"),bg=BG,fg=TEXT_PRI); self._lbl_page.pack(side="left")
        self._badge=tk.Label(sbar,text="",font=(FONT,10,"bold"),bg=BG,fg=BG,padx=10,pady=3); self._badge.pack(side="left",padx=(10,0))
        self._lbl_extra=tk.Label(sbar,text="",font=(FONT,9),bg=BG,fg=TEXT_SEC); self._lbl_extra.pack(side="left",padx=(12,0))
        self._lbl_counter=tk.Label(sbar,text="",font=(FONT,9),bg=BG,fg=TEXT_SEC); self._lbl_counter.pack(side="right")
        nav=tk.Frame(self,bg=BG,padx=20,pady=4); nav.pack(fill="x")
        self._btn_back=tk.Button(nav,text="◀  Back",command=self._on_back,font=(FONT,10,"bold"),bg="#E5E7EB",fg=TEXT_PRI,relief="flat",bd=0,padx=14,pady=8,width=10,cursor="hand2",state="disabled"); self._btn_back.pack(side="left")
        self._btn_next=tk.Button(nav,text="Next  ▶",command=self._on_next,font=(FONT,10,"bold"),bg=ACCENT,fg=BTN_FG,relief="flat",bd=0,padx=14,pady=8,width=10,cursor="hand2",state="disabled"); self._btn_next.pack(side="left",padx=(8,0))
        self._btn_reset=tk.Button(nav,text="Reset",command=self._on_reset,font=(FONT,10,"bold"),bg="#E5E7EB",fg=TEXT_PRI,relief="flat",bd=0,padx=14,pady=8,width=7,cursor="hand2",state="disabled"); self._btn_reset.pack(side="left",padx=(8,0))
        tk.Button(nav, text="Exit", command=self.destroy, font=(FONT, 10, "bold"), bg="#374151", fg=BTN_FG, relief="flat", bd=0, padx=14, pady=8, width=7, cursor="hand2").pack(side="left", padx=(8,0))
        self._lbl_faults=tk.Label(nav,text="",font=(FONT,10),bg=BG,fg=FAULT_FG); self._lbl_faults.pack(side="right",padx=(10,0))
        self._lbl_hits=tk.Label(nav,text="",font=(FONT,10),bg=BG,fg=HIT_FG); self._lbl_hits.pack(side="right")
        ho=tk.Frame(self,bg=BG,padx=20); ho.pack(fill="both",expand=True,pady=(6,16))
        tk.Label(ho,text="STEP HISTORY",font=(FONT,8,"bold"),bg=BG,fg=TEXT_SEC).pack(anchor="w",pady=(0,6))
        tbl=tk.Frame(ho,bg=SURFACE,highlightthickness=1,highlightbackground=BORDER); tbl.pack(fill="both",expand=True)
        hdr=tk.Frame(tbl,bg=ACCENT_L); hdr.pack(fill="x")
        for txt,w in [("#",4),("Page",6),("Frames after (LRU→MRU)",34),("Status",10)]:
            tk.Label(hdr,text=txt,font=(FONT,9,"bold"),bg=ACCENT_L,fg=ACCENT,width=w,anchor="center",pady=6).pack(side="left")
        self._hist_canvas=tk.Canvas(tbl,bg=SURFACE,highlightthickness=0)
        vsb=tk.Scrollbar(tbl,orient="vertical",command=self._hist_canvas.yview)
        self._hist_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right",fill="y"); self._hist_canvas.pack(side="left",fill="both",expand=True)
        self._hist_inner=tk.Frame(self._hist_canvas,bg=SURFACE)
        cwin=self._hist_canvas.create_window((0,0),window=self._hist_inner,anchor="nw")
        self._hist_inner.bind("<Configure>",lambda e:self._hist_canvas.configure(scrollregion=self._hist_canvas.bbox("all")))
        self._hist_canvas.bind("<Configure>",lambda e,c=cwin:self._hist_canvas.itemconfig(c,width=e.width))

    def _rebuild_cells(self,cap):
        for w in self._cells_frame.winfo_children(): w.destroy()
        self._cells=[]
        for _ in range(cap):
            cell=tk.Frame(self._cells_frame,bg=SURFACE,width=70,height=70,highlightthickness=1,highlightbackground=BORDER)
            cell.pack(side="left",padx=(0,8)); cell.pack_propagate(False)
            lbl=tk.Label(cell,text="—",font=(FONT,20,"bold"),bg=SURFACE,fg=EMPTY_FG); lbl.place(relx=.5,rely=.45,anchor="center")
            sub=tk.Label(cell,text="",font=(FONT,7),bg=SURFACE,fg=TEXT_SEC); sub.place(relx=.5,rely=.82,anchor="center")
            self._cells.append((cell,lbl,sub))

    def _update_cells(self,frames_data,status):
        items=[(p,None) for p in frames_data]
        cbg=HIT_BG if status=="HIT" else FAULT_BG; cfg=HIT_FG if status=="HIT" else FAULT_FG
        for i,(cell,lbl,sub) in enumerate(self._cells):
            if i<len(items):
                pg,_=items[i]; active=pg==self._cur_page
                bg=cbg if active else SURFACE; fg=cfg if active else TEXT_PRI
                cell.config(bg=bg); lbl.config(text=str(pg),bg=bg,fg=fg); sub.config(text="",bg=bg)
            else:
                cell.config(bg=SURFACE); lbl.config(text="—",bg=SURFACE,fg=EMPTY_FG); sub.config(text="",bg=SURFACE)

    def _add_hist_row(self,idx,entry):
        bg=HIT_BG if entry["status"]=="HIT" else FAULT_BG; fg=HIT_FG if entry["status"]=="HIT" else FAULT_FG
        fs="  ".join(str(p) for p in entry["frames"])
        row=tk.Frame(self._hist_inner,bg=bg); row.pack(fill="x")
        for txt,w,a in [(str(idx+1),4,"center"),(str(entry["page"]),6,"center"),(fs,34,"center"),(entry["status"],10,"center")]:
            tk.Label(row,text=txt,font=("Consolas",10),bg=bg,fg=(fg if txt==entry["status"] else TEXT_PRI),width=w,anchor=a,pady=5).pack(side="left")
        tk.Frame(self._hist_inner,bg=BORDER,height=1).pack(fill="x")

    def _on_start(self):
        raw=self.ref_var.get().replace(","," ").split()
        if not raw: messagebox.showerror("Error","Reference string is empty."); return
        try: pages=[int(p) for p in raw]
        except ValueError: messagebox.showerror("Error","All pages must be integers."); return
        self._capacity=self.cap_var.get()
        self._faults,self._hits,self._log=run_algorithm(pages,self._capacity)
        self._step=-1; self._rebuild_cells(self._capacity)
        for w in self._hist_inner.winfo_children(): w.destroy()
        self._lbl_page.config(text=""); self._badge.config(text="",bg=BG); self._lbl_extra.config(text="")
        self._lbl_counter.config(text=f"0 / {len(self._log)} steps"); self._lbl_hits.config(text=""); self._lbl_faults.config(text="")
        self._btn_next.config(state="normal"); self._btn_back.config(state="disabled"); self._btn_reset.config(state="normal")

    def _on_next(self):
        if self._step<len(self._log)-1: self._step+=1; self._render(self._step)
        if self._step==len(self._log)-1: self._btn_next.config(state="disabled")
        self._btn_back.config(state="normal")

    def _on_back(self):
        if self._step>0:
            self._step-=1
            for w in self._hist_inner.winfo_children(): w.destroy()
            for i in range(self._step+1): self._add_hist_row(i,self._log[i])
            self._render(self._step,add_hist=False)
        if self._step==0: self._btn_back.config(state="disabled")
        self._btn_next.config(state="normal")

    def _on_reset(self):
        self._step=-1; self._rebuild_cells(self._capacity)
        for w in self._hist_inner.winfo_children(): w.destroy()
        self._lbl_page.config(text=""); self._badge.config(text="",bg=BG); self._lbl_extra.config(text="")
        self._lbl_counter.config(text=f"0 / {len(self._log)} steps"); self._lbl_hits.config(text=""); self._lbl_faults.config(text="")
        self._btn_next.config(state="normal"); self._btn_back.config(state="disabled")

    def _render(self,idx,add_hist=True):
        entry=self._log[idx]; self._cur_page=entry["page"]
        self._update_cells(entry["frames"],entry["status"])
        self._lbl_page.config(text=f"Page  {entry['page']}")
        if entry["status"]=="HIT": self._badge.config(text=" HIT ",bg=HIT_FG,fg=BTN_FG)
        else: self._badge.config(text=" FAULT ",bg=FAULT_FG,fg=BTN_FG)
        self._lbl_extra.config(text=entry.get("extra",""))
        faults=sum(1 for e in self._log[:idx+1] if e["status"]=="FAULT")
        hits=sum(1 for e in self._log[:idx+1] if e["status"]=="HIT")
        self._lbl_counter.config(text=f"Step {idx+1} / {len(self._log)}")
        self._lbl_hits.config(text=f"Hits {hits}   "); self._lbl_faults.config(text=f"Faults {faults}   ")
        if add_hist: self._add_hist_row(idx,entry); self._hist_canvas.yview_moveto(1.0)

if __name__=="__main__":
    App().mainloop()

#! /usr/bin/python
# -*- coding: UTF-8 -*-

# See AUTHORS file for further information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# If not, see <http://www.gnu.org/licenses/>.

# data una lista di parole e loro immagine le presenta una a una in una pagina html e aggiorna
# il testo mapped sulla base dell'input dell'utente


# dato un testo mapped corretto aggiorna lo strato testo del file djvu


# finds a substring beginning with idi and ending with idf; returns it
# with (dc=1) or without (default dc=0) idi and idf; used for xml managing too

# Nuova versione, gestisce i tag annidati; x e' la parte "aspecifica" del
# tag di apertura (es: {{ cercando {{Intestazione| )


def find_stringa(stringa,idi,idf,dc=0,x=None,side="left"): # This is my beloved routine, I couldn't live without it! 
    if side=="right":
        idip=stringa.rfind(idi)
    else:
        idip=stringa.find(idi)
    idfp=stringa.find(idf,idip+len(idi))+len(idf)
    if idip>-1 and idfp>0:
        if x!=None:
            while stringa[idip:idfp].count(x)>stringa[idip:idfp].count(idf):
                if stringa[idip:idfp].count(x)>stringa[idip:idfp].count(idf):
                    idfp=stringa.find(idf,idfp)+len(idf)
                
        if dc==0:
            vvalore=stringa[idip+len(idi):idfp-len(idf)]
        else:
            vvalore=stringa[idip:idfp]
    else:
        vvalore=""
    return vvalore


# restituisce la stringa idi...ifd "a cavallo" di offset
# senza (dc=0) o con (dc!=0) i delimitatori idi...idf
        
def find_r(stringa,idi,idf,offset,dc=1):
    idip=stringa.rfind(idi,0,offset)
    idfp=stringa.find(idf,idip+len(idi))+len(idf)
    if idip>-1 and idfp>0:
        if dc==0:
            vvalore=stringa[idip+len(idi):idfp-len(idf)]
        else:
            vvalore=stringa[idip:idfp]
    else:
        vvalore=""
    return vvalore

def produci_lista(testo,idi,idf,dc=1,inizio=None):
    t=testo[:]
    lista=[]
    while not find_stringa(t,idi,idf)=="":
        el=find_stringa(t,idi,idf,1,x=inizio)
        t=t.replace(el,"")
        if dc==0:
            el=find_stringa(el,idi,idf,0,x=inizio)
        lista.append(el)
    return lista
import streamlit as st
import requests

# ==========================================
# 🎨 1. 고급 편집숍 레트로 감성 CSS 주입 (한글 폰트 무드 고도화)
# ==========================================
st.markdown("""
    <style>
    /* 영문 Playfair와 가장 닮은, 획의 대비가 강하고 클래식한 한글 서체 로드 */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=ChosunGu:wght@400&family=Nanum+Myeongjo:wght@400;700;800&display=swap');
    
    .stApp {
        background-color: #f7f4eb; /* 은은한 크림 베이지 바탕 */
        color: #2b2b2b;
    }
    
    /* 제목 스타일 (Ginva Font 느낌의 클래식 세리프) */
    h1 {
        font-family: 'Playfair Display', 'Nanum Myeongjo', serif !important;
        font-weight: 800 !important;
        color: #1a2a3a !important; /* 빈티지 네이비 포인트 */
        letter-spacing: -1px;
        text-align: center;
        margin-bottom: 5px !important;
    }
    
    .subtitle {
        font-family: 'Playfair Display', 'Nanum Myeongjo', serif;
        text-align: center;
        color: #8c826e;
        font-size: 13px;
        letter-spacing: 1px;
        margin-bottom: 40px;
    }
    
    /* 일반 텍스트, 라벨 폰트 스타일 변경 (영어 서체 같은 정갈함 유지) */
    .stMarkdown, p, label, div {
        font-family: 'Nanum Myeongjo', serif;
    }
    
    /* 라디오 버튼 스타일 */
    .stRadio div[role="radiogroup"] {
        justify-content: center;
        gap: 20px;
    }
    
    /* 깔끔한 가로선 선택 버튼 (Streamlit Button 커스텀) */
    div.stButton > button {
        background-color: transparent;
        color: #2b4c7e;
        border: 1px solid #2b4c7e;
        border-radius: 2px;
        font-family: 'Nanum Myeongjo', serif;
        font-size: 12px;
        padding: 2px 10px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #2b4c7e;
        color: #ffffff;
        border: 1px solid #2b4c7e;
    }
    
    /* 더보기(Expander) 스타일 정돈 */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border: 1px solid #e0dacb !important;
        border-radius: 2px !important;
        font-family: 'Nanum Myeongjo', serif;
        font-size: 12px !important;
        color: #6e6552 !important;
    }
    
    /* 얇은 선 느낌의 매치 리스트 스타일 (4번 사진의 라인 일러스트 감성) */
    .recommend-item {
        border-bottom: 1px solid #e0dacb;
        padding: 12px 5px;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .recommend-index {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        color: #8c826e;
        margin-right: 15px;
    }
    .recommend-title {
        font-weight: 700;
        color: #1a2a3a;
    }
    .recommend-artist {
        color: #8c826e;
        font-size: 12px;
        margin-left: 8px;
    }
    .recommend-match {
        font-family: 'Playfair Display', serif;
        font-weight: bold;
        color: #2b4c7e; /* 빈티지 블루 포인트 */
        font-size: 12px;
        border: 1px solid #2b4c7e;
        padding: 1px 5px;
        border-radius: 2px;
        letter-spacing: 0.5px;
    }
    
    /* 메트릭 박스 감성 스케일 다운 */
    .metric-box {
        background-color: #ffffff;
        border: 1px solid #e0dacb;
        padding: 15px;
        border-radius: 2px;
        text-align: center;
    }
    .metric-label {
        font-family: 'Playfair Display', serif;
        font-size: 11px;
        color: #8c826e;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 14px;
        font-weight: 700;
        color: #1a2a3a;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧱 2. 본문 레이아웃 및 기능
# ==========================================

st.markdown("<h1>minim recommendation</h1>", unsafe_allow_html=True)
st.markdown("<p class=\"subtitle\">선택된 음악과 아티스트를 위한 에디토리얼 큐레이션 서비스</p>", unsafe_allow_html=True)

# 1. 검색 모드 선택
search_mode = st.radio(
    "SELECT MODE",
    ("MUSIC", "ARTIST"),
    horizontal=True
)

# 사용자 입력 받기
if search_mode == "MUSIC":
    label_text = "노래 제목을 입력하세요 (영어로 입력 시 정확도가 높습니다):"
    default_text = "Dynamite"
else:
    label_text = "가수 이름을 입력하세요 (영어로 입력 시 정확도가 높습니다):"
    default_text = "NewJeans"

search_query = st.text_input(label_text, default_text)

if search_query:
    API_KEY = "b25b959554ed76058ac220b7b2e0a026"
    
    try:
        # ==========================================
        # CASE A: 음악 검색 모드 (중복 곡 가수 선택 기능 포함)
        # ==========================================
        if search_mode == "MUSIC":
            search_url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={search_query}&api_key={API_KEY}&format=json&limit=8"
            response = requests.get(search_url).json()
            tracks = response.get('results', {}).get('trackmatches', {}).get('track', [])
            
            if tracks:
                st.write("")
                st.markdown("<div style='font-size:12px; color:#8c826e; margin-bottom:10px;'>검색된 곡 목록 중 일치하는 아티스트를 선택해 주세요:</div>", unsafe_allow_html=True)
                
                # 중복된 곡명/가수 리스트를 버튼 형태로 렌더링
                selected_track = None
                for idx, t in enumerate(tracks):
                    t_name = t['name']
                    a_name = t['artist']
                    
                    # 가독성을 높인 리스트 스타일 내에 선택 버튼 배치
                    col_text, col_btn = st.columns([4, 1])
                    with col_text:
                        st.markdown(f"<div style='padding: 5px 0; font-size:14px;'>🎵 <b>{t_name}</b> <span style='color:#6e6552;'>- {a_name}</span></div>", unsafe_allow_html=True)
                    with col_btn:
                        # 각각의 버튼에 고유 키값을 부여하여 클릭 감지
                        if st.button("선택 후 추천", key=f"track_{idx}"):
                            selected_track = t
                
                # 버튼을 누르거나 혹은 검색 후 아무것도 안 눌렀을 땐 첫 번째 항목을 기본값으로 타겟팅 유지
                if 'active_track' not in st.session_state or search_query != st.session_state.get('last_query'):
                    st.session_state['active_track'] = tracks[0]
                    st.session_state['last_query'] = search_query
                
                if selected_track:
                    st.session_state['active_track'] = selected_track
                
                # 활성화된 트랙 정보 가져오기
                final_track = st.session_state['active_track']
                track_name = final_track['name']
                artist_name = final_track['artist']
                
                st.markdown("---")
                st.markdown(f"<div style='text-align:center; color:#2b4c7e; font-size:14px; margin-bottom:25px;'>— 분석 중인 큐레이션 레코드: <b>{track_name}</b> by {artist_name} —</div>", unsafe_allow_html=True)
                
                # 곡 상세 정보 가져오기
                detail_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getinfo&track={track_name}&artist={artist_name}&api_key={API_KEY}&format=json"
                detail_response = requests.get(detail_url).json()
                track_info = detail_response.get('track', {})
                
                tags = track_info.get('toptags', {}).get('tag', [])
                genres = [tag['name'] for tag in tags[:2]] if tags else ["N/A"]
                
                duration = track_info.get('duration', '0')
                try:
                    duration_sec = int(duration) // 1000
                    if duration_sec == 0: duration_sec = int(duration)
                    duration_str = f"{duration_sec // 60}m {duration_sec % 60}s" if duration_sec > 0 else "N/A"
                except:
                    duration_str = "N/A"
                
                # 📊 미니멀 요약 정보 오버뷰
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<div class='metric-box'><div class='metric-label'>GENRE</div><div class='metric-value'>{genres[0].upper()}</div></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='metric-box'><div class='metric-label'>DURATION</div><div class='metric-value'>{duration_str}</div></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div class='metric-box'><div class='metric-label'>ARTIST</div><div class='metric-value'>{artist_name}</div></div>", unsafe_allow_html=True)
                
                st.write("")
                with st.expander("VIEW DETAILED LOGS (상세 수치 기록 더보기)"):
                    st.markdown(f"""
                    <div style="font-size: 13px; line-height: 1.8; color: #6e6552;">
                        • <b>Track:</b> {track_name}<br>
                        • <b>Artist:</b> {artist_name}<br>
                        • <b>Playcount:</b> {int(track_info.get('playcount', 0)):,} 회 누적 재생<br>
                        • <b>Listeners:</b> {int(track_info.get('listeners', 0)):,} 명 청취 완료
                    </div>
                    """, unsafe_allow_html=True)
                
                # 비슷한 곡 추천받기
                sim_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&track={track_name}&artist={artist_name}&api_key={API_KEY}&format=json&limit=15"
                sim_response = requests.get(sim_url).json()
                sim_tracks = sim_response.get('similartracks', {}).get('track', [])
                
                st.markdown("<br><h3 style='font-family:\"Playfair Display\", serif; font-size:16px; color:#1a2a3a; border-bottom: 2px solid #1a2a3a; padding-bottom:5px; letter-spacing:1px;'>POPULAR SIMILAR TRACKS</h3>", unsafe_allow_html=True)
                
                if sim_tracks:
                    for idx, rec_track in enumerate(sim_tracks[:15]):
                        rec_name = rec_track['name']
                        rec_artist = rec_track['artist']['name']
                        similarity = rec_track.get('match', '0')
                        
                        try:
                            sim_percent = f"{float(similarity) * 100:.0f}%"
                        except:
                            sim_percent = "N/A"
                        
                        st.markdown(f"""
                        <div class="recommend-item">
                            <div>
                                <span class="recommend-index">{idx + 1:02d}</span>
                                <span class="recommend-title">{rec_name}</span>
                                <span class="recommend-artist">by {rec_artist}</span>
                            </div>
                            <div class="recommend-match">{sim_percent}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("추천 데이터를 찾지 못했습니다.")

        # ==========================================
        # CASE B: 가수 검색 모드
        # ==========================================
        elif search_mode == "ARTIST":
            search_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.search&artist={search_query}&api_key={API_KEY}&format=json&limit=1"
            response = requests.get(search_url).json()
            artists = response.get('results', {}).get('artistmatches', {}).get('artist', [])
            
            if artists:
                top_artist = artists[0]
                artist_name = top_artist['name']
                
                st.markdown(f"<div style='text-align:center; color:#2b4c7e; font-size:14px; margin-bottom:20px;'>— Selected Artist: <b>{artist_name}</b> —</div>", unsafe_allow_html=True)
                
                detail_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={API_KEY}&format=json"
                detail_response = requests.get(detail_url).json()
                artist_info = detail_response.get('artist', {})
                
                tags = artist_info.get('tags', {}).get('tag', [])
                genres = [tag['name'] for tag in tags[:2]] if tags else ["N/A"]
                listeners = artist_info.get('stats', {}).get('listeners', '0')
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div class='metric-box'><div class='metric-label'>MAIN GENRE</div><div class='metric-value'>{genres[0].upper()}</div></div>", unsafe_allow_html=True)
                with col2:
                    try: listeners_val = f"{int(listeners):,}"
                    except: listeners_val = listeners
                    st.markdown(f"<div class='metric-box'><div class='metric-label'>TOTAL LISTENERS</div><div class='metric-value'>{listeners_val}</div></div>", unsafe_allow_html=True)
                
                st.write("")
                bio_content = artist_info.get('bio', {}).get('summary', '소개 정보가 없습니다.')
                with st.expander("VIEW BIOGRAPHY (아티스트 히스토리 더보기)"):
                    st.markdown(f"""
                    <div style="font-size: 13px; color: #6e6552; line-height: 1.8;">
                        {bio_content}<br><br>
                        • <b>Total Playcount:</b> {int(artist_info.get('stats', {}).get('playcount', 0)):,} 회 재생 기록
                    </div>
                    """, unsafe_allow_html=True)
                
                sim_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={artist_name}&api_key={API_KEY}&format=json&limit=15"
                sim_response = requests.get(sim_url).json()
                sim_artists = sim_response.get('similarartists', {}).get('artist', [])
                
                st.markdown("<br><h3 style='font-family:\"Playfair Display\", serif; font-size:16px; color:#1a2a3a; border-bottom: 2px solid #1a2a3a; padding-bottom:5px; letter-spacing:1px;'>SIMILAR ARTISTS</h3>", unsafe_allow_html=True)
                
                if sim_artists:
                    for idx, rec_artist_obj in enumerate(sim_artists[:15]):
                        rec_artist_name = rec_artist_obj['name']
                        similarity = rec_artist_obj.get('match', '0')
                        
                        try: sim_percent = f"{float(similarity) * 100:.0f}%"
                        except: sim_percent = "N/A"
                        
                        st.markdown(f"""
                        <div class="recommend-item">
                            <div>
                                <span class="recommend-index">{idx + 1:02d}</span>
                                <span class="recommend-title">{rec_artist_name}</span>
                            </div>
                            <div class="recommend-match">{sim_percent}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("추천 데이터를 찾지 못했습니다.")
            else:
                st.error("아티스트를 찾을 수 없습니다.")
                
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
successfully downloaded text file (SHA: f12df0fbc35e4fe7be538e529555f6f31ba9cf8d)import streamlit as st
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
    
    /* 아이템 카드 내 x 버튼 스타일 */
    .item-delete-btn {
        position: absolute;
        top: 2px;
        right: 2px;
        background: none;
        border: none;
        color: #ffffff;
        font-size: 18px;
        cursor: pointer;
        padding: 0;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .item-delete-btn:hover {
        color: #ffcccc;
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
    
    /* 그리드 카드 스타일 */
    .card {
        background-color: #ffffff;
        border: 1px solid #e0dacb;
        border-radius: 4px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }
    .card:hover {
        border-color: #2b4c7e;
        box-shadow: 0 2px 8px rgba(43, 76, 126, 0.1);
    }
    .card-title {
        font-weight: 700;
        color: #1a2a3a;
        font-size: 14px;
        margin-bottom: 8px;
        word-break: break-word;
    }
    .card-artist {
        color: #8c826e;
        font-size: 12px;
        margin-bottom: 10px;
    }
    .card-match {
        background-color: #2b4c7e;
        color: #ffffff;
        padding: 4px 8px;
        border-radius: 2px;
        font-size: 11px;
        font-weight: bold;
        display: inline-block;
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

# 세션 상태 초기화
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []
if 'item_list' not in st.session_state:
    st.session_state.item_list = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = search_mode

# 모드가 변경되면 item_list 초기화
if search_mode != st.session_state.current_mode:
    st.session_state.item_list = []
    st.session_state.search_query = ""
    st.session_state.search_results = []
    st.session_state.show_results = False
    st.session_state.current_mode = search_mode

API_KEY = "b25b959554ed76058ac220b7b2e0a026"

# 사용자 입력 받기
if search_mode == "MUSIC":
    label_text = "노래 제목을 입력하세요 (영어로 입력 시 정확도가 높습니다):"
    placeholder_text = "Dynamite"
else:
    label_text = "가수 이름을 입력하세요 (영어로 입력 시 정확도가 높습니다):"
    placeholder_text = "NewJeans"

col_input, col_btn = st.columns([4, 1])
with col_input:
    search_query = st.text_input(label_text, value=st.session_state.search_query, placeholder=placeholder_text, key="search_input")
with col_btn:
    add_item = st.button("+ ADD", use_container_width=True)

# 아이템 추가 함수
def add_search_item(selected_item=None):
    if search_mode == "ARTIST":
        # 아티스트 모드: 검색 없이 바로 추가
        if search_query and search_query.strip():
            st.session_state.item_list.append({
                'query': search_query,
                'mode': search_mode,
                'id': len(st.session_state.item_list),
                'name': search_query,
                'artist': None
            })
            st.session_state.search_results = []
            st.session_state.show_results = False
            st.session_state.search_query = ""  # 입력값 초기화
    else:
        # 음악 모드: 선택된 항목 추가
        if selected_item:
            st.session_state.item_list.append({
                'query': selected_item['name'],
                'mode': search_mode,
                'id': len(st.session_state.item_list),
                'name': selected_item['name'],
                'artist': selected_item['artist']
            })
            st.session_state.search_results = []
            st.session_state.show_results = False
            st.session_state.search_query = ""  # 입력값 초기화

if add_item and search_query:
    if search_mode == "ARTIST":
        add_search_item()
        st.rerun()
    else:
        # 음악 모드: 검색 실행
        with st.spinner("[...] searching..."):
            search_url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={search_query}&api_key={API_KEY}&format=json&limit=10"
            response = requests.get(search_url).json()
            tracks = response.get('results', {}).get('trackmatches', {}).get('track', [])
            st.session_state.search_results = tracks
            st.session_state.show_results = True
        st.rerun()

# 음악 검색 결과 표시 및 선택
if search_mode == "MUSIC" and st.session_state.show_results and st.session_state.search_results:
    st.markdown("<p style='font-size: 13px; color: #8c826e; margin-top: 15px; margin-bottom: 10px;'>[*] search results - select correct track:</p>", unsafe_allow_html=True)
    
    for idx, track in enumerate(st.session_state.search_results):
        col_track, col_select = st.columns([4, 1])
        with col_track:
            st.markdown(f"""
            <div style='background-color: #ffffff; border: 1px solid #e0dacb; padding: 10px; border-radius: 2px;'>
                <div style='font-weight: bold; color: #1a2a3a;'>{track['name']}</div>
                <div style='color: #8c826e; font-size: 12px;'>by {track['artist']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_select:
            if st.button("SELECT", key=f"select_{idx}", use_container_width=True):
                add_search_item(track)
                st.rerun()

# 선택된 아이템 표시 (멀티 선택)
if st.session_state.item_list:
    st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:\"Nanum Myeongjo\", serif; font-size: 12px; color: #8c826e; margin: 0 0 12px 0;'>[+] selected items</p>", unsafe_allow_html=True)
    
    # 2칼럼으로 아이템 표시
    cols = st.columns(2)
    for idx, item in enumerate(st.session_state.item_list):
        with cols[idx % 2]:
            artist_info = f"by {item['artist']}" if item.get('artist') else ""
            col_item, col_del = st.columns([5, 1])
            
            with col_item:
                st.markdown(f"""
                <div style='background-color: #2b4c7e; padding: 12px; border-radius: 2px; color: #ffffff; font-size: 13px; margin-right: 8px;'>
                    <div style='font-weight: bold; color: #ffffff;'>[♪] {item['name']}</div>
                    <div style='color: #dfe5ed; font-size: 11px; margin-top: 4px;'>{artist_info}</div>
                    <div style='color: #b8c5d6; font-size: 10px; margin-top: 3px;'>{item['mode']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_del:
                if st.button("✕", key=f"del_btn_{item['id']}", use_container_width=True, help="Remove"):
                    st.session_state.item_list.remove(item)
                    st.rerun()
    
    # 초기화 버튼
    if st.button("[↻] RESET ALL", use_container_width=False):
        st.session_state.item_list = []
        st.session_state.search_query = ""
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# 공통점 분석 시작
if st.session_state.item_list and len(st.session_state.item_list) >= 2:
    analyze_button = st.button("[◆] ANALYZE & RECOMMEND", use_container_width=True)
else:
    st.info("Please select 2 or more songs/artists")
    analyze_button = False

if analyze_button and st.session_state.item_list:
    
    try:
        # 모든 아이템 정보 수집
        items_data = []
        all_genres = []
        
        with st.spinner("[...] collecting data..."):
            for item in st.session_state.item_list:
                if item['mode'] == "MUSIC":
                    # 이미 선택된 곡 정보 사용
                    track_name = item['name']
                    artist_name = item['artist']
                    
                    # 곡 상세정보
                    detail_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getinfo&track={track_name}&artist={artist_name}&api_key={API_KEY}&format=json"
                    detail_response = requests.get(detail_url).json()
                    track_info = detail_response.get('track', {})
                    
                    tags = track_info.get('toptags', {}).get('tag', [])
                    genres = [tag['name'].lower() for tag in tags]
                    all_genres.extend(genres)
                    
                    items_data.append({
                        'type': 'MUSIC',
                        'name': track_name,
                        'artist': artist_name,
                        'genres': genres,
                        'full_info': track_info
                    })
                
                else:  # ARTIST mode - 입력값 그대로 사용
                    artist_name = item['name']
                    
                    # 아티스트 상세정보
                    detail_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.search&artist={artist_name}&api_key={API_KEY}&format=json&limit=1"
                    search_response = requests.get(detail_url).json()
                    artists = search_response.get('results', {}).get('artistmatches', {}).get('artist', [])
                    
                    if artists:
                        artist = artists[0]
                        artist_found_name = artist['name']
                        
                        detail_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_found_name}&api_key={API_KEY}&format=json"
                        detail_response = requests.get(detail_url).json()
                        artist_info = detail_response.get('artist', {})
                        
                        tags = artist_info.get('tags', {}).get('tag', [])
                        genres = [tag['name'].lower() for tag in tags]
                        all_genres.extend(genres)
                        
                        items_data.append({
                            'type': 'ARTIST',
                            'name': artist_found_name,
                            'genres': genres,
                            'full_info': artist_info
                        })
                    else:
                        items_data.append({
                            'type': 'ARTIST',
                            'name': artist_name,
                            'genres': [],
                            'full_info': {}
                        })
        
        # ==========================================
        # 공통점 분석
        # ==========================================
        from collections import Counter
        
        st.markdown("---")
        st.markdown("<h3 style='font-family:\"Playfair Display\", serif; font-size:16px; color:#1a2a3a; border-bottom: 2px solid #1a2a3a; padding-bottom:5px; letter-spacing:1px;'>[#] DATA ANALYSIS</h3>", unsafe_allow_html=True)
        
        # 선택된 아이템 요약
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-box'><div class='metric-label'>ITEMS SELECTED</div><div class='metric-value'>{len(items_data)}</div></div>", unsafe_allow_html=True)
        
        # 공통 장르 찾기
        genre_counter = Counter(all_genres)
        common_genres = [g for g, count in genre_counter.items() if count >= len(items_data) * 0.5]  # 50% 이상 공통
        most_common = genre_counter.most_common(3)
        
        with col2:
            if common_genres:
                st.markdown(f"<div class='metric-box'><div class='metric-label'>COMMON GENRE</div><div class='metric-value'>{common_genres[0].upper()}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='metric-box'><div class='metric-label'>COMMON GENRE</div><div class='metric-value'>NONE</div></div>", unsafe_allow_html=True)
        
        # 세부 정보
        with st.expander("[≡] ITEM DETAILS"):
            for item in items_data:
                st.markdown(f"<div style='padding: 10px; border-bottom: 1px solid #e0dacb;'>", unsafe_allow_html=True)
                if item['type'] == 'MUSIC':
                    st.markdown(f"<b>[♪] {item['name']}</b> - {item['artist']}<br><small style='color: #8c826e;'>Genres: {', '.join(item['genres'][:3]) if item['genres'] else 'none'}</small>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<b>[○] {item['name']}</b><br><small style='color: #8c826e;'>Genres: {', '.join(item['genres'][:3]) if item['genres'] else 'none'}</small>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # 공통점 메시지
        if common_genres:
            st.success(f"[✓] Common point found! - {', '.join([g.upper() for g in common_genres[:3]])}")
        else:
            st.warning(f"[!] No common genres - selected items have very different styles")
            st.info(f"[•] Top genres: {' / '.join([f'{m[0].upper()}' for m in most_common[:3]])}")
        
        # ==========================================
        # 공통점 기반 추천
        # ==========================================
        st.markdown("<br><h3 style='font-family:\"Playfair Display\", serif; font-size:16px; color:#1a2a3a; border-bottom: 2px solid #1a2a3a; padding-bottom:5px; letter-spacing:1px;'>[→] RECOMMENDATIONS</h3>", unsafe_allow_html=True)
        
        if common_genres or most_common:
            # 추천 기준 설정
            search_genre = common_genres[0] if common_genres else most_common[0][0]
            
            # 유사 곡/아티스트 수집
            similar_items = []
            for item in items_data:
                if item['type'] == 'MUSIC':
                    sim_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&track={item['name']}&artist={item['artist']}&api_key={API_KEY}&format=json&limit=10"
                    sim_response = requests.get(sim_url).json()
                    sim_tracks = sim_response.get('similartracks', {}).get('track', [])
                    for track in sim_tracks:
                        similar_items.append({
                            'name': track['name'],
                            'artist': track['artist']['name'],
                            'match': float(track.get('match', 0))
                        })
                else:
                    sim_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={item['name']}&api_key={API_KEY}&format=json&limit=10"
                    sim_response = requests.get(sim_url).json()
                    sim_artists = sim_response.get('similarartists', {}).get('artist', [])
                    for artist in sim_artists:
                        similar_items.append({
                            'name': artist['name'],
                            'match': float(artist.get('match', 0))
                        })
            
            # 중복 제거 및 정렬
            unique_similar = {}
            for item in similar_items:
                key = item['name']
                if key not in unique_similar:
                    unique_similar[key] = item
                else:
                    unique_similar[key]['match'] = max(unique_similar[key]['match'], item['match'])
            
            sorted_similar = sorted(unique_similar.values(), key=lambda x: x['match'], reverse=True)[:15]
            
            if sorted_similar:
                st.markdown(f"<p style='font-size: 12px; color: #8c826e; margin-bottom: 20px;'>[•] Similar to '{search_genre.upper()}' - in grid view</p>", unsafe_allow_html=True)
                
                # 그리드 레이아웃 (3칼럼)
                cols = st.columns(3)
                for idx, rec in enumerate(sorted_similar):
                    with cols[idx % 3]:
                        match_percent = f"{rec['match'] * 100:.0f}%"
                        artist_info = f"{rec['artist']}" if 'artist' in rec else "Unknown"
                        
                        st.markdown(f"""
                        <div class="card">
                            <div class="card-title">[♪] {rec['name']}</div>
                            <div class="card-artist">{artist_info}</div>
                            <div class="card-match">{match_percent}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("[!] No recommendation data found.")
        else:
            st.error("[!] Analysis error - no data found.")

                
    except Exception as e:
        st.error(f"[!] Error occurred: {str(e)}")

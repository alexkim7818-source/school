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

# 세션 상태 초기화
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []
if 'item_list' not in st.session_state:
    st.session_state.item_list = []

# 사용자 입력 받기
if search_mode == "MUSIC":
    label_text = "노래 제목을 입력하세요 (영어로 입력 시 정확도가 높습니다):"
    placeholder_text = "Dynamite"
else:
    label_text = "가수 이름을 입력하세요 (영어로 입력 시 정확도가 높습니다):"
    placeholder_text = "NewJeans"

col_input, col_btn = st.columns([4, 1])
with col_input:
    search_query = st.text_input(label_text, placeholder_text)
with col_btn:
    add_item = st.button("➕ 추가하기", use_container_width=True)

# 아이템 추가 함수
def add_search_item():
    if search_query and search_query.strip():
        st.session_state.item_list.append({
            'query': search_query,
            'mode': search_mode,
            'id': len(st.session_state.item_list)
        })

if add_item and search_query:
    add_search_item()
    st.rerun()

# 선택된 아이템 표시 (멀티 선택)
if st.session_state.item_list:
    st.markdown("<div style='margin-top: 20px; padding: 15px; background-color: #ffffff; border: 1px solid #e0dacb; border-radius: 2px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:\"Nanum Myeongjo\", serif; font-size: 12px; color: #8c826e; margin: 0 0 10px 0;'>선택된 항목 (여러 개 선택 가능)</p>", unsafe_allow_html=True)
    
    cols = st.columns(len(st.session_state.item_list) + 1)
    for idx, item in enumerate(st.session_state.item_list):
        with cols[idx]:
            st.markdown(f"""
            <div style='background-color: #f7f4eb; padding: 8px; border-radius: 2px; text-align: center; font-size: 11px; border-left: 3px solid #2b4c7e;'>
                <div style='font-weight: bold; color: #1a2a3a;'>{item['query']}</div>
                <div style='color: #8c826e; font-size: 10px;'>{item['mode']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✕", key=f"del_{item['id']}", use_container_width=True):
                st.session_state.item_list.remove(item)
                st.rerun()
    
    # 초기화 버튼
    with cols[-1]:
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.item_list = []
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# 공통점 분석 시작
if st.session_state.item_list and len(st.session_state.item_list) >= 2:
    analyze_button = st.button("🔍 공통점 분석 & 추천", use_container_width=True)
else:
    st.info("2개 이상의 곡/가수를 선택해주세요")
    analyze_button = False

if analyze_button and st.session_state.item_list:
    API_KEY = "b25b959554ed76058ac220b7b2e0a026"
    
    try:
        # 모든 아이템 정보 수집
        items_data = []
        all_genres = []
        
        with st.spinner("🔄 데이터 수집 중..."):
            for item in st.session_state.item_list:
                if item['mode'] == "MUSIC":
                    search_url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={item['query']}&api_key={API_KEY}&format=json&limit=1"
                    response = requests.get(search_url).json()
                    tracks = response.get('results', {}).get('trackmatches', {}).get('track', [])
                    
                    if tracks:
                        track = tracks[0]
                        track_name = track['name']
                        artist_name = track['artist']
                        
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
                
                else:  # ARTIST mode
                    search_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.search&artist={item['query']}&api_key={API_KEY}&format=json&limit=1"
                    response = requests.get(search_url).json()
                    artists = response.get('results', {}).get('artistmatches', {}).get('artist', [])
                    
                    if artists:
                        artist = artists[0]
                        artist_name = artist['name']
                        
                        # 아티스트 상세정보
                        detail_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={API_KEY}&format=json"
                        detail_response = requests.get(detail_url).json()
                        artist_info = detail_response.get('artist', {})
                        
                        tags = artist_info.get('tags', {}).get('tag', [])
                        genres = [tag['name'].lower() for tag in tags]
                        all_genres.extend(genres)
                        
                        items_data.append({
                            'type': 'ARTIST',
                            'name': artist_name,
                            'genres': genres,
                            'full_info': artist_info
                        })
        
        # ==========================================
        # 공통점 분석
        # ==========================================
        from collections import Counter
        
        st.markdown("---")
        st.markdown("<h3 style='font-family:\"Playfair Display\", serif; font-size:16px; color:#1a2a3a; border-bottom: 2px solid #1a2a3a; padding-bottom:5px; letter-spacing:1px;'>📊 공통점 분석</h3>", unsafe_allow_html=True)
        
        # 선택된 아이템 요약
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-box'><div class='metric-label'>선택된 항목</div><div class='metric-value'>{len(items_data)}</div></div>", unsafe_allow_html=True)
        
        # 공통 장르 찾기
        genre_counter = Counter(all_genres)
        common_genres = [g for g, count in genre_counter.items() if count >= len(items_data) * 0.5]  # 50% 이상 공통
        most_common = genre_counter.most_common(3)
        
        with col2:
            if common_genres:
                st.markdown(f"<div class='metric-box'><div class='metric-label'>공통 장르</div><div class='metric-value'>{common_genres[0].upper()}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='metric-box'><div class='metric-label'>공통 장르</div><div class='metric-value'>없음</div></div>", unsafe_allow_html=True)
        
        # 세부 정보
        with st.expander("📋 선택된 항목 정보"):
            for item in items_data:
                st.markdown(f"<div style='padding: 10px; border-bottom: 1px solid #e0dacb;'>", unsafe_allow_html=True)
                if item['type'] == 'MUSIC':
                    st.markdown(f"<b>🎵 {item['name']}</b> - {item['artist']}<br><small style='color: #8c826e;'>장르: {', '.join(item['genres'][:3]) if item['genres'] else '없음'}</small>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<b>👤 {item['name']}</b><br><small style='color: #8c826e;'>장르: {', '.join(item['genres'][:3]) if item['genres'] else '없음'}</small>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # 공통점 메시지
        if common_genres:
            st.success(f"✅ 공통점 발견! 공통 장르: {', '.join([g.upper() for g in common_genres[:3]])}")
        else:
            st.warning("⚠️ 공통 장르 없음 - 선택한 항목들의 음악 스타일이 매우 다릅니다")
            st.info(f"💡 각 항목의 주요 장르: {' / '.join([f'{m[0].upper()}' for m in most_common[:3]])}")
        
        # ==========================================
        # 공통점 기반 추천
        # ==========================================
        st.markdown("<br><h3 style='font-family:\"Playfair Display\", serif; font-size:16px; color:#1a2a3a; border-bottom: 2px solid #1a2a3a; padding-bottom:5px; letter-spacing:1px;'>🎯 공통점 기반 추천</h3>", unsafe_allow_html=True)
        
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
                st.markdown(f"<p style='font-size: 12px; color: #8c826e;'>🎧 '{search_genre.upper()}' 장르와 비슷한 추천:</p>", unsafe_allow_html=True)
                for idx, rec in enumerate(sorted_similar):
                    match_percent = f"{rec['match'] * 100:.0f}%"
                    artist_info = f" - {rec['artist']}" if 'artist' in rec else ""
                    st.markdown(f"""
                    <div class="recommend-item">
                        <div>
                            <span class="recommend-index">{idx + 1:02d}</span>
                            <span class="recommend-title">{rec['name']}</span>
                            <span class="recommend-artist">{artist_info}</span>
                        </div>
                        <div class="recommend-match">{match_percent}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("추천 데이터를 찾지 못했습니다.")
        else:
            st.error("분석 오류: 데이터를 찾을 수 없습니다.")

                
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
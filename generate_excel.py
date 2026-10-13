import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_guide():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove default blank sheet

    FONT_FAMILY = "Meiryo UI"
    
    # Monotone Palette Definitions
    # Headers: Dark Charcoal & Slate Gray
    # Accent: Muted Medium Gray & Light Gray Fills
    # Text: Near Black (#1A1A1A / #262626)
    font_title = Font(name=FONT_FAMILY, size=15, bold=True, color="FFFFFF")
    font_section = Font(name=FONT_FAMILY, size=11.5, bold=True, color="1F1F1F")
    font_header = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    font_bold = Font(name=FONT_FAMILY, size=9.5, bold=True, color="1A1A1A")
    font_regular = Font(name=FONT_FAMILY, size=9.0, bold=False, color="262626")
    font_emphasis = Font(name=FONT_FAMILY, size=9.0, bold=True, color="000000")
    font_small = Font(name=FONT_FAMILY, size=8.5, bold=False, color="4A4A4A")
    
    fill_title = PatternFill(start_color="212121", end_color="212121", fill_type="solid")       # #212121 (Pitch Charcoal)
    fill_header = PatternFill(start_color="3D3D3D", end_color="3D3D3D", fill_type="solid")      # #3D3D3D (Dark Charcoal)
    fill_sub_header = PatternFill(start_color="5A5A5A", end_color="5A5A5A", fill_type="solid")  # #5A5A5A (Medium Charcoal)
    fill_stripe = PatternFill(start_color="F5F5F5", end_color="F5F5F5", fill_type="solid")      # #F5F5F5 (Light Gray)
    fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")       # #FFFFFF (White)
    fill_highlight = PatternFill(start_color="EBEBEB", end_color="EBEBEB", fill_type="solid")   # #EBEBEB (Soft Accent Gray)
    fill_box = PatternFill(start_color="DFDFDF", end_color="DFDFDF", fill_type="solid")         # #DFDFDF (Box Accent)

    border_thin = Side(style='thin', color="CCCCCC")
    border_medium = Side(style='medium', color="3D3D3D")
    border_double = Side(style='double', color="3D3D3D")

    cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)
    header_border = Border(left=border_thin, right=border_thin, top=border_medium, bottom=border_double)
    box_border = Border(left=border_medium, right=border_medium, top=border_medium, bottom=border_medium)

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)

    # -------------------------------------------------------------
    # SHEET 1: 01_概要・小学生向け解説
    # -------------------------------------------------------------
    ws1 = wb.create_sheet(title="01_概要・小学生向け解説")
    ws1.views.sheetView[0].showGridLines = True

    ws1.merge_cells("A1:G1")
    ws1["A1"] = "JBoss EAP 8.1 (IronJacamar) と AWS RDS Proxy コネクションプール徹底解説"
    ws1["A1"].font = font_title
    ws1["A1"].fill = fill_title
    ws1["A1"].alignment = align_center
    ws1.row_dimensions[1].height = 38

    ws1["A2"] = "■ はじめに：なぜECSタスク内のコンテナとRDSの間に「2重のコネクションプール」が存在するのか？"
    ws1["A2"].font = font_section
    ws1.row_dimensions[2].height = 24

    ws1.merge_cells("A3:G3")
    ws1["A3"] = (
        "現代のエンタープライズクラウドシステム（Amazon ECS上のマルチコンテナ構成）では、Javaアプリケーションサーバー（JBoss EAP 8.1）の"
        "内部プールである「IronJacamar（アイアンジャカマー）」と、AWSのマネージド中間プロキシである「RDS Proxy」が協調して動作します。\n"
        "「プールが2箇所にあるのは無駄では？」と思われがちですが、それぞれが担当する階層（レイヤー）、保護する対象、プーリングしている実体"
        "（JVM内Javaオブジェクト vs DB側物理プロセス/ソケット）が根本から異なり、両者が揃って初めて「超高速応答」と「DB枯渇防止・無瞬断フェイルオーバー」が両立します。"
    )
    ws1["A3"].font = font_regular
    ws1["A3"].fill = fill_highlight
    ws1["A3"].alignment = align_left
    ws1["A3"].border = box_border
    ws1.row_dimensions[3].height = 55

    ws1["A5"] = "■ 小学生でも完全に直感できる！「超わかりやすい学校のたとえ話」"
    ws1["A5"].font = font_section
    ws1.row_dimensions[5].height = 24

    headers1 = ["登場キャラクター", "現実世界の役割", "ITシステムの正体", "小学生向け解説（なにをしている人？）", "もしこの人がいなかったらどうなる？"]
    ws1.row_dimensions[6].height = 26
    for col_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=6, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    meta_rows = [
        ("校長先生", "学校で一番大事な記録を持つ人", "データベース本体\n(Amazon RDS / Aurora)", 
         "全校生徒のテストの点数や通知表を金庫で守っている人。とても頭が良いけれど、一度に何百人もの生徒から一斉に話しかけられると耳がパンクして倒れてしまいます。", 
         "生徒たちが一斉に話しかけると校長先生が気絶（CPU 100%、メモリ枯渇）してしまい、学校全体がストップ（システム全停止）してしまいます。"),
        
        ("1年1組\n(フロント係)", "学校の玄関でお客さんを迎える教室", "フロントコンテナ\n(BFF / Web API)", 
         "外から学校に来る保護者やお客さん（スマホやPC）を最初に笑顔で迎える教室。お客さんが増えると、自動で1組、2組、3組と教室が増えます（ECSオートスケール）。", 
         "教室が足りなくなると、玄関にお客さんの大行列ができてしまいます。"),
        
        ("1年2組\n(バック係)", "奥の部屋で難しい計算をする教室", "バックコンテナ\n(業務ドメイン / バッチ)", 
         "フロント係から「この計算お願い！」と頼まれて、大事なお金の計算や帳簿付けをじっくり行う教室。こちらも忙しくなると自動で教室が増えます。", 
         "計算係がパンクすると、学校の大事な手続きがすべて止まってしまいます。"),
        
        ("学級委員長\n(IronJacamar)", "各教室にある【内線電話メモ】を管理する係", "JBoss EAP 8.1内の\nコネクションプール", 
         "各教室（フロント・バックの各コンテナ）の中に1人ずついます。\n教室の生徒（処理スレッド）が校長先生に電話したいとき、いちいち校長室まで走って電線を引いて電話機を買いに行く（TCP接続＋認証）のは時間がかかりすぎます！\nそこで学級委員長があらかじめ「机の上に3本の受話器」をキープしておき、「使いたい人はどうぞ！終わったら受話器を机に戻してね」と貸し出してくれます。", 
         "生徒が質問するたびに毎回新しい電話線を引くことになり、生徒が疲れ果てて質問がめちゃくちゃ遅くなります（応答遅延）。"),
        
        ("スーパー受付秘書\n(RDS Proxy)", "校長室のドアの前で電話を取り次ぐプロ", "AWS RDS Proxy\n(マネージド中間プロキシ)", 
         "全校生徒と校長先生の間に立つ、超優秀な受付のお姉さん！\nもし学校全体で100クラスに増えたら、学級委員長の電話（3本×100クラス＝300本！）が一斉に校長室にかかってきます。校長先生は電話を取るだけで倒れます。\nそこで受付秘書さんが校長室の前に立ち、300本の電話を全部一人で一旦受け止めます。校長先生とは「秘書専用のたった20本の内線」だけで繋ぎ、生徒Aの短い質問（0.1秒）が終わったら、即座に同じ内線で生徒Bの質問を取り次ぎます（多重化）。さらに校長先生が交代（フェイルオーバー）しても、秘書さんが裏でサッと繋ぎ替えるので、生徒は誰も気づきません！", 
         "クラスが増えた瞬間に校長室の電話が鳴り止まず、校長先生が即死します。校長先生が交代するときに全クラスの電話がプツンと切れて大パニックになります！")
    ]

    for r_idx, r_data in enumerate(meta_rows, 7):
        ws1.row_dimensions[r_idx].height = 64
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws1.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 2, 3] else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx in [1, 2, 3] else align_left
            cell.border = cell_border

    ws1.cell(row=13, column=1, value="■ なぜ「両方」必要なのか？ ひとくち結論").font = font_section
    ws1.row_dimensions[13].height = 24

    ws1.merge_cells("A14:G14")
    summary_box = (
        "【IronJacamarの目的】コンテナ内部のJavaスレッドが、ミリ秒以下の極小レイテンシで接続オブジェクトを借りて返すため（アプリ視点の超高速化）\n"
        "【RDS Proxyの目的】大量に増殖したコンテナから押し寄せる膨大なTCP接続からDB本体のメモリ・CPUを守り、DB障害時も切断させないため（DB視点の絶対防御）"
    )
    ws1["A14"] = summary_box
    ws1["A14"].font = font_emphasis
    ws1["A14"].fill = fill_box
    ws1["A14"].alignment = align_left
    ws1["A14"].border = box_border
    ws1.row_dimensions[14].height = 40

    col_widths1 = {1: 18, 2: 24, 3: 24, 4: 55, 5: 45, 6: 15, 7: 15}
    for col_idx, width in col_widths1.items():
        ws1.column_dimensions[get_column_letter(col_idx)].width = width

    # -------------------------------------------------------------
    # SHEET 2: 02_歴史とアーキテクチャ立ち位置
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="02_歴史とアーキテクチャ立ち位置")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:G1")
    ws2["A1"] = "登場の歴史的変遷とシステムアーキテクチャ上の立ち位置"
    ws2["A1"].font = font_title
    ws2["A1"].fill = fill_title
    ws2["A1"].alignment = align_center
    ws2.row_dimensions[1].height = 38

    ws2["A2"] = "■ 1. 接続技術の歴史的変遷：なぜIronJacamarが生まれ、なぜRDS Proxyが必要になったのか？"
    ws2["A2"].font = font_section
    ws2.row_dimensions[2].height = 24

    hist_headers = ["世代", "時代背景・システム形態", "接続方式", "生じた課題とボトルネック", "解決策と技術の誕生"]
    ws2.row_dimensions[3].height = 26
    for c_idx, h in enumerate(hist_headers, 1):
        cell = ws2.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    hist_data = [
        ("第1世代\n(1990年代)", "CGI / 初期のJava Web\n(Web黎明期)", "都度接続\n(Direct Connect)",
         "HTTPリクエストが来るたびに「TCP 3-way handshake」「SSL/TLSネゴシエーション」「DBユーザー認証」「DB側プロセス生成」を実行。\n接続確立だけで数ミリ秒〜数十ミリ秒を要し、リクエスト集中でDBがプロセスフォークに耐えきれず即死。",
         "都度接続を廃止し、接続をあらかじめ作って再利用する「コネクションプーリング」の概念が誕生。"),
        
        ("第2世代\n(2000〜2010年代)", "Java EE / 巨大モノリスAPサーバー\n(JBoss AS / EAP)", "アプリ内コネクションプール\n(JCA / IronJacamar)",
         "巨大な単一JVM内で数十〜数百スレッドがDBにアクセス。J2EE/Jakarta EE標準としてJCA (Java Connector Architecture) が制定。\nJBoss AS 7 / EAP 6以降、高度なトランザクション連携・XA分散トランザクション・リーク検知を備えた「IronJacamar」が標準エンジンとして君臨。\n【当時の前提】サーバー台数が数台固定だったため、アプリ内プールだけでDB保護が完全に成立していた。",
         "JVM内で接続オブジェクトを保持・貸出。物理接続を閉じずにプールへ返却することでDB接続オーバーヘッドをゼロ化。"),
        
        ("第3世代\n(2015年代〜)", "Docker / Amazon ECS / マイクロサービス\n(コンテナ分散時代)", "コンテナ毎の独立IronJacamar\n(プールの増殖問題)",
         "モノリスが分解され、フロントコンテナ（BFF/Web）とバックコンテナ（Domain/Batch）に分離。\nさらにオートスケーリングでコンテナが10台、50台、100台と自律的に増減。\n各コンテナのIronJacamarが個別に min=10, max=50 を保持すると、100コンテナ×50＝5,000接続がDBに殺到！\nPostgreSQLのプロセスモデル（1接続＝1プロセス、約10MB消費）やMySQLのスレッドモデルの限界を超え、DBがメモリ枯渇・コンテキストスイッチ激増でダウン。",
         "「コンテナ内部だけのプールでは、クラウドの急激なスケールアウトに対応できない」という致命的限界が顕在化。"),
        
        ("第4世代\n(2020年代〜現在)", "クラウドネイティブ / サーバーレス / ECS\n(2層プーリングアーキテクチャ)", "IronJacamar ＋ AWS RDS Proxy\n(協調動作モデル)",
         "コンテナ側はIronJacamarで極小レイテンシで処理しつつ、DB手前にAWSマネージドな「RDS Proxy」を配置。\nRDS Proxyが何千本ものコンテナ接続を集約し、バックエンドDBには少数の最適接続数（例: 数十〜数百本）で多重化（Multiplexing）してクエリを転送。\nさらにAuroraフェイルオーバー時の無瞬断ルーティング、IAM認証オフロードを実現。",
         "【現在の決定版】クライアント側プール（IronJacamar）とサーバー側プール（RDS Proxy）の役割分担による完全解決。")
    ]

    for r_idx, r_data in enumerate(hist_data, 4):
        ws2.row_dimensions[r_idx].height = 68
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws2.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 3] else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx in [1, 3] else align_left
            cell.border = cell_border

    ws2.cell(row=9, column=1, value="■ 2. ECSフロント／バックコンテナにおけるIronJacamarとRDS Proxyの立ち位置比較").font = font_section
    ws2.row_dimensions[9].height = 24

    role_headers = ["比較項目", "フロントコンテナ内 IronJacamar", "バックコンテナ内 IronJacamar", "AWS RDS Proxy (マネージド層)"]
    ws2.row_dimensions[10].height = 26
    for c_idx, h in enumerate(role_headers, 1):
        cell = ws2.cell(row=10, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    role_data = [
        ("配置場所 (レイヤー)", "ECSタスク内 フロントコンテナのJVMヒープ", "ECSタスク内 バックコンテナのJVMヒープ", "AWS VPC内 マネージドインフラ層 (Multi-AZ)"),
        ("インスタンス単位", "フロントコンテナごとに1つ独立して存在", "バックコンテナごとに1つ独立して存在", "VPC内で統合された単一の論理エンドポイント"),
        ("スケーリングの挙動", "フロントのタスク数増減に連動してプール数が増減", "バックのタスク数増減に連動してプール数が増減", "トラフィックに応じてAWSが裏で自律スケーリング"),
        ("主な処理特性", "短時間クエリ、画面参照、セッション管理、高並行性", "複雑なトランザクション、バッチ更新、整合性重視", "全コンテナからのTCP接続の終端と多重化ルーティング"),
        ("接続相手", "RDS Proxyのエンドポイント (Port 3306/5432)", "RDS Proxyのエンドポイント (Port 3306/5432)", "RDS / Aurora データベース本体のWriter/Reader"),
        ("トランザクション管理", "JTAローカルトランザクションまたは非トランザクション", "JTA / XA 分散トランザクション連携、2相コミット", "トランザクション中の接続固定 (Session Pinning)"),
        ("障害時の役割", "切断検知時のリトライ、プールフラッシュ", "XA未決着トランザクションのリカバリ、ロールバック", "Aurora障害時の新Writerへの自動・高速切り替え (66%短縮)"),
        ("セキュリティ担当", "JBoss Elytron によるクレデンシャル管理", "JBoss Elytron によるクレデンシャル管理", "AWS Secrets Manager連携、IAM認証、TLS強制")
    ]

    for r_idx, r_data in enumerate(role_data, 11):
        ws2.row_dimensions[r_idx].height = 32
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws2.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx == 1 else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx == 1 else align_left
            cell.border = cell_border

    col_widths2 = {1: 22, 2: 36, 3: 36, 4: 45, 5: 35}
    for col_idx, width in col_widths2.items():
        ws2.column_dimensions[get_column_letter(col_idx)].width = width

    # -------------------------------------------------------------
    # SHEET 3: 03_プーリング情報詳細比較
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="03_プーリング情報詳細比較")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:E1")
    ws3["A1"] = "IronJacamar と RDS Proxy がプーリング（保持）している情報の徹底対比"
    ws3["A1"].font = font_title
    ws3["A1"].fill = fill_title
    ws3["A1"].alignment = align_center
    ws3.row_dimensions[1].height = 38

    ws3["A2"] = "■ プーリングしている実体とメモリ保持構造の相違点（Javaヒープ vs ネットワーク/カーネル）"
    ws3["A2"].font = font_section
    ws3.row_dimensions[2].height = 24

    info_headers = ["分類", "保持する情報の名称", "IronJacamar (JBoss EAP 8.1)", "AWS RDS Proxy", "なぜプーリング（キャッシュ）するのか？"]
    ws3.row_dimensions[3].height = 26
    for c_idx, h in enumerate(info_headers, 1):
        cell = ws3.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    pool_info_data = [
        ("ネットワーク／ソケット", "物理TCP/TLS接続ソケット", 
         "コンテナJVM〜RDS Proxy間のTCPソケット。\nJavaのSocketImplとしてJVMヒープ内に保持。", 
         "RDS Proxy〜RDS本体間の物理TCPソケット。\nProxyのLinuxカーネルソケットバッファで保持。", 
         "TCP 3-way ハンドシェイクおよびTLSネゴシエーションの高コストな通信往復をスキップするため。"),
        
        ("認証・クレデンシャル", "認証済みセッション情報", 
         "JBoss ElytronのSubject情報、暗号化キーストアから復号したDBユーザー名/パスワード。", 
         "AWS Secrets Managerから取得・キャッシュしたDBマスターパスワード、IAMトークン検証結果。", 
         "クエリごとにパスワード認証やIAM認可処理をやり直すオーバーヘッドを防止するため。"),
        
        ("アプリケーション層", "接続ラッパーオブジェクト\n(Connection Handle)", 
         "org.jboss.jca...WrappedConnection オブジェクト。\nアプリが close() を呼んでもソケットを閉じず、プールに返却するインターセプト用プロキシ。", 
         "プーリングしない。\n（RDS ProxyはJDBCを知らないため、プロトコルレベルのパケットとして処理）", 
         "Java標準のJDBCインターフェース仕様を保ちつつ、物理接続の破棄を横取りして再利用するため。"),
        
        ("SQL／ステートメント", "PreparedStatement キャッシュ\n(構文解析ツリー)", 
         "PreparedStatementCache オブジェクト。\nSQL文文字列と引数型をキーに、DBドライバが解析した実行計画・バイナリ文をヒープにキャッシュ。", 
         "プロキシ内部でのキャッシュ機能あり。\n※ただしPostgreSQLで拡張プロトコルを利用するとセッションピニングの引き金になるため注意が必要。", 
         "DB側でのSQL構文解析（Parse/Analyze/Rewrite）を省略し、SQL実行時間を劇的に短縮するため。"),
        
        ("トランザクション", "トランザクション同期情報\n(JTA / XA Resource)", 
         "XAResource、TransactionImpl、Xid（グローバルトランザクションID）との関連付け。\n同一TX内での接続再利用（track-connection-by-tx）。", 
         "セッションピニング状態フラグ。\nトランザクション中（BEGIN〜COMMIT）は特定のバックエンド接続をクライアントに占有させる。", 
         "ACID特性を保証するため。トランザクション中の操作が別のDB接続に分散して不整合を起こすのを防ぐ。"),
        
        ("状態管理／セッション", "セッション状態変数\n(Session Variables)", 
         "プーリングしない。\n（IronJacamarはSQLの中身やDB変数の状態には不干渉）", 
         "SET文（PostgreSQLの SET search_path、MySQLの SET autocommit 等）や一時テーブルの追跡情報。\n状態変更があれば「Pinned」としてマーク。", 
         "多重化時に、あるコンテナが変更したセッション設定が別のコンテナのクエリに誤って引き継がれるのを防止する防壁。"),
        
        ("ヘルスチェック", "健全性・検証ステータス\n(Validation State)", 
         "最終バリデーション実行時刻、エラー発生回数、割り当て経過時間、リーク追跡スタックトレース。", 
         "バックエンドDB接続のヘルスチェック結果、Auroraトポロジー状態（Writer/Readerロール）。", 
         "ハングした接続や、DBフェイルオーバーで死んだ「ゾンビ接続」をアプリが掴んでエラーになるのを防ぐため。")
    ]

    for r_idx, r_data in enumerate(pool_info_data, 4):
        ws3.row_dimensions[r_idx].height = 55
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws3.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 2] else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx in [1, 2] else align_left
            cell.border = cell_border

    col_widths3 = {1: 20, 2: 24, 3: 40, 4: 40, 5: 35}
    for col_idx, width in col_widths3.items():
        ws3.column_dimensions[get_column_letter(col_idx)].width = width

    # -------------------------------------------------------------
    # SHEET 4: 04_IronJacamar設定値詳説
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="04_IronJacamar設定値詳説")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:G1")
    ws4["A1"] = "JBoss EAP 8.1 (IronJacamar) データソース・プール設定パラメータ詳説"
    ws4["A1"].font = font_title
    ws4["A1"].fill = fill_title
    ws4["A1"].alignment = align_center
    ws4.row_dimensions[1].height = 38

    ws4["A2"] = "■ standalone.xml / JBoss CLI におけるデータソースプール完全定義リファレンス"
    ws4["A2"].font = font_section
    ws4.row_dimensions[2].height = 24

    param_headers = ["XMLタグ / 属性名", "JBoss CLI 属性名", "型 / 単位", "デフォルト値", "ECS×RDS Proxy推奨値", "パラメータの役割と動作原理", "設定時の重要注意点・最新知見"]
    ws4.row_dimensions[3].height = 26
    for c_idx, h in enumerate(param_headers, 1):
        cell = ws4.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    ij_params = [
        ("<min-pool-size>", "min-pool-size", "int (個数)", "0", "3 〜 5 (タスク規模による)", 
         "プール内にアイドル状態で常時維持する最小物理接続数。", 
         "ECSでコンテナが大量にオートスケールする場合、大きな値を設定すると「タスク数×min-pool-size」でProxyへの待機接続が膨らむため、比較的小さめ（3〜5程度）に抑えるのが最新のベストプラクティス。"),
        
        ("<initial-pool-size>", "initial-pool-size", "int (個数)", "0", "min-pool-sizeと同値", 
         "サーバー（コンテナ）起動時に即座に作成する初期接続数。", 
         "prefill=true と併用することで、コンテナ起動直後の最初のリクエストでの接続確立レイテンシをゼロにし、コールドスタートを防ぐ。"),
        
        ("<max-pool-size>", "max-pool-size", "int (個数)", "20", "10 〜 20", 
         "プールが許容する最大物理接続数。これを超えるとスレッドは空き待ちキューに並ぶ。", 
         "フロント/バックのワーカースレッド数および同時実行可能リクエスト数に合わせて設定。「ECS最大タスク数 × max-pool-size」がRDS Proxyの許容クライアント接続数（デフォルト無制限/メモリ上限）を超えないよう計算する。"),
        
        ("<prefill>", "pool-prefill", "boolean", "false", "true", 
         "サーバー起動時に min-pool-size まで接続をあらかじめ満たしておくかどうかのフラグ。", 
         "ECSのタスク起動時、ヘルスチェックが通過した直後に本番リクエストが殺到しても接続作成遅延を起こさないよう、必ず true に設定を推奨。"),
        
        ("<flush-strategy>", "flush-strategy", "enum", "FailingConnectionOnly", "FailingConnectionOnly\nまたは IdleConnections", 
         "エラー検知や手動フラッシュ時にプール内の接続をどう破棄するかのポリシー。\n・FailingConnectionOnly: 異常が発生した接続のみ破棄\n・IdleConnections: アイドル接続のみ破棄\n・EntirePool: プール全破棄\n・Gracefully: 使用中接続を待って破棄", 
         "RDS Proxy環境では、Proxy側がフェイルオーバー時に壊れた接続を検知するため、健全な接続まで巻き込んで破棄しない FailingConnectionOnly が最も安全で高スループット。"),
        
        ("<blocking-timeout-wait-millis>", "blocking-timeout-wait-millis", "long (ミリ秒)", "30000\n(30秒)", "5000 〜 10000\n(5〜10秒)", 
         "max-pool-size に達している状態で、空き接続ができるのをスレッドが待機する最大許容時間。", 
         "デフォルトの30秒は長すぎる。プール枯渇時にスレッドが30秒間滞留すると、Undertowのワーカースレッドが枯渇してコンテナ全体が道連れで無応答になる。5〜10秒でフェイルファストさせ、呼び出し元にエラーを返すのが鉄則。"),
        
        ("<idle-timeout-minutes>", "idle-timeout-minutes", "long (分)", "15", "5 〜 10", 
         "接続が使われなくなってから破棄されるまでのアイドル許容時間（min-pool-sizeを超える余剰接続が対象）。", 
         "★超重要！ RDS Proxyの「IdleClientTimeout（デフォルト30分）」よりも【必ず短い時間】に設定すること！\nもしProxy側が先に切断すると、IronJacamarが切断されたことに気付かず、次に使おうとして通信エラー（Connection reset）が発生する。"),
        
        ("<background-validation>", "background-validation", "boolean", "false", "true", 
         "バックグラウンドスレッドが定期的にプール内の接続の疎通を確認するかどうか。", 
         "必ず true を推奨。次の background-validation-millis とセットで動かすことで、アイドル接続が生きているかを常時監視し、死んだ接続をアプリリクエストが引くのを完全に防止する。"),
        
        ("<background-validation-millis>", "background-validation-millis", "long (ミリ秒)", "0", "30000 〜 60000\n(30〜60秒)", 
         "バックグラウンド検証を実行するインターバル周期。", 
         "短すぎるとProxyやDBに不要な Ping パケットが飛び、長すぎるとProxy側の切断を検知できない。30秒〜60秒が最適なバランス。"),
        
        ("<validate-on-match>", "validate-on-match", "boolean", "false", "false", 
         "アプリケーションが getConnection() を呼んで接続を借りるたびに、毎回DB疎通確認を行うフラグ。", 
         "★要注意！ RDS Proxy環境では「必ず false」にすること！\nこれを true にすると、クエリを発行するたびに毎回「SELECT 1」等の検証クエリがProxyに飛び、多重化効率が激減し、レイテンシが大幅に悪化する。検証はバックグラウンドに任せる。"),
        
        ("<valid-connection-checker>", "valid-connection-checker-class-name", "class", "なし", "DB専用クラス\n(MySQL/PostgreSQL用)", 
         "JDBCドライバ固有の高速Pingプロトコルを用いて接続健全性を検証するJBoss拡張クラス。", 
         "SELECT 1 を投げるよりもネットワークパケットが小さく、DBエンジンに負荷をかけずに高速検証可能。\n例: org.jboss.jca.adapters.jdbc.extensions.postgres.PostgreSQLValidConnectionChecker"),
        
        ("<prepared-statement-cache-size>", "prepared-statement-cache-size", "int (個数)", "0", "0 〜 30 (環境による)", 
         "接続ごとにJVMヒープ内でキャッシュするプリペアドステートメントの最大数。", 
         "★PostgreSQL + RDS Proxy環境での最大トラップ！\nPostgreSQLドライバで名前付きステートメントをキャッシュすると、RDS Proxyが「セッションピニング」を起こして多重化を解除してしまう場合がある。ピニング率（CloudWatch）を監視して調整が必要。"),
        
        ("<track-connection-by-tx>", "track-connection-by-tx", "boolean", "false", "true", 
         "同一トランザクション内で行われる複数回の getConnection() に対して、常に同一の物理接続を割り当てるフラグ。", 
         "バックコンテナでトランザクション整合性を厳密に保つために必須。JTAトランザクションが完了するまで同一接続に固定される。"),

        ("<capacity-incrementer-class>", "capacity-incrementer-class", "class", "なし", "標準インクリメンタ", 
         "プール拡張時に一度にいくつの接続を追加するかを決定するポリシー拡張クラス。", 
         "急激なバーストアクセス時に1本ずつではなく複数本まとめて接続を作成し、待機スレッドのレイテンシを平滑化する。"),

        ("システムプロパティ\n(ironjacamar.mcp)", "システムプロパティ", "String", "なし", "LeakDumperManagedConnectionPool\n(検証環境推奨)", 
         "プール管理実装をリーク検知用クラスに差し替えるプロパティ。\n-Dironjacamar.mcp=...LeakDumperManagedConnectionPool", 
         "クローズされずに放置されたコネクションを検知し、取得時のスタックトレースをログ出力する。本番投入前のリーク洗い出しに絶大な威力を発揮。")
    ]

    for r_idx, r_data in enumerate(ij_params, 4):
        ws4.row_dimensions[r_idx].height = 48
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws4.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 4, 5] else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx in [3, 4, 5] else align_left
            cell.border = cell_border

    col_widths4 = {1: 28, 2: 28, 3: 16, 4: 18, 5: 22, 6: 42, 7: 48}
    for col_idx, width in col_widths4.items():
        ws4.column_dimensions[get_column_letter(col_idx)].width = width

    # -------------------------------------------------------------
    # SHEET 5: 05_RDSProxy設定値詳説
    # -------------------------------------------------------------
    ws5 = wb.create_sheet(title="05_RDSProxy設定値詳説")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells("A1:G1")
    ws5["A1"] = "AWS RDS Proxy 設定パラメータ詳説（ターゲットグループ ＆ プロキシ設定）"
    ws5["A1"].font = font_title
    ws5["A1"].fill = fill_title
    ws5["A1"].alignment = align_center
    ws5.row_dimensions[1].height = 38

    ws5["A2"] = "■ AWSマネジメントコンソール / AWS CLI / Terraform における完全設定リファレンス"
    ws5["A2"].font = font_section
    ws5.row_dimensions[2].height = 24

    proxy_param_headers = ["パラメータ名 (API/CLI)", "設定対象", "型 / 単位", "デフォルト値", "推奨設定値", "パラメータの役割と動作原理", "設定時の重要注意点・最新知見"]
    ws5.row_dimensions[3].height = 26
    for c_idx, h in enumerate(proxy_param_headers, 1):
        cell = ws5.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    rds_proxy_params = [
        ("MaxConnectionsPercent", "Target Group", "Percentage\n(1〜100%)", "100%", "70% 〜 80%", 
         "データベース本体（RDS/Aurora）の max_connections に対して、RDS Proxyがバックエンド接続として開くことを許可する最大割合。", 
         "★超重要！ 絶対に100%のまま放置してはいけない！\n100%にするとProxyがDB接続を使い切り、運用管理者の踏み台接続やモニタリングツール、自動メンテナンスタスクが接続できなくなる。20〜30%は管理者枠として空けておくため70〜80%に設定するのがAWS推奨。"),
        
        ("MaxIdleConnectionsPercent", "Target Group", "Percentage\n(0〜100%)", "50%", "20% 〜 50%", 
         "ProxyがDB本体との間で「アイドル状態」として保持・維持しておくバックエンド接続の最大割合（MaxConnectionsPercentに対する割合）。", 
         "トラフィックの急増（スパイク）に備えてウォーム接続を保持する。アクセスが常に安定している場合は20〜30%に下げてDB側のメモリを節約し、アクセス変動が激しいWebシステムでは50%を維持して接続遅延を防ぐ。"),
        
        ("ConnectionBorrowTimeout", "Target Group", "Seconds\n(0〜300秒)", "120秒", "10 〜 30秒", 
         "クライアント（コンテナ）からクエリが来た際、Proxy内のバックエンド接続がすべて使用中で空きがない場合に、接続が空くまで待機する上限時間。", 
         "デフォルト120秒は長すぎる。DB過負荷時にコンテナ側が2分間も待たされると、JBossのHTTPスレッドが完全にスタックする。IronJacamarの blocking-timeout-wait-millis（例: 10秒）と同等か少し長めの15〜30秒に短縮すべき。"),
        
        ("IdleClientTimeout", "Proxy Config", "Seconds\n(1〜28800秒)", "1800秒\n(30分)", "1800秒 (30分)\nまたは 3600秒 (1時間)", 
         "クライアント（コンテナのIronJacamar）とRDS Proxy間のTCP接続が無通信のままアイドル状態を維持できる最大時間。", 
         "★タイムアウト逆転の防止！\n前述の通り、JBossの idle-timeout-minutes（例: 10分）より必ず大きくすること。Proxyが先に無言切断すると、コンテナ側で「Broken pipe」や「Connection reset」エラーが頻発する。"),
        
        ("SessionPinningFilters", "Target Group\n(MySQLのみ)", "List of Strings", "空 (なし)", "EXCLUDE_VARIABLE_SETS\n(要件に応じる)", 
         "MySQLにおいて、特定のセッション状態変更操作（SET文など）をセッションピニングのトリガーから除外するフィルター設定。", 
         "MySQL利用時に、ORM（Hibernateなど）が安全なセッション変数を設定しただけでピニングされて多重化が解除されるのを防ぎ、高い多重化性能を維持できる。"),
        
        ("InitQuery", "Target Group", "String", "空 (なし)", "SET time_zone = 'Asia/Tokyo'\nなど", 
         "ProxyがバックエンドDBとの間に新しい物理接続を確立するたびに、自動的に1回だけ実行する初期化SQL文。", 
         "全セッション共通で必要な環境設定（タイムゾーンや文字コード等）をここで1回だけ実行しておくことで、アプリ側が毎回 SET 文を発行してセッションピニングを起こすのを回避できる。"),
        
        ("RequireTLS", "Proxy Config", "Boolean", "true", "true", 
         "コンテナ〜RDS Proxy間の通信において、SSL/TLS暗号化接続を必須とするかどうかの設定。", 
         "コンテナとDB間の通信セキュリティ（盗聴・改ざん防止）のために true を強く推奨。JBoss側のデータソースURLにも sslMode / useSSL パラメータを整合させる。"),
        
        ("Auth (IAM / Secrets Manager)", "Proxy Config", "JSON Config", "Secrets Manager ARN", "Secrets Manager\n＋ IAM認証併用", 
         "RDS ProxyがDB本体に接続する際の認証情報連携。Secrets Managerで自動ローテーションされるパスワードを利用。", 
         "コンテナ側にDBパスワードを持たせる必要がなくなる（コンテナ〜Proxy間はIAMタスクロール認証が可能）。パスワード変更時もコンテナの再起動が完全に不要。"),

        ("DebugLogging", "Proxy Config", "Boolean", "false", "トラブル調査時のみ true", 
         "CloudWatch LogsにProxyの接続ハンドシェイク、多重化、セッションピニングのトリガー詳細ログを出力するフラグ。", 
         "本番定常運用で有効にするとログ料金が高騰するため通常はfalse。検証環境やピニング原因追究時にtrueに設定して詳細分析を行う。")
    ]

    for r_idx, r_data in enumerate(rds_proxy_params, 4):
        ws5.row_dimensions[r_idx].height = 48
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(rds_data := r_data, 1):
            cell = ws5.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 3, 4, 5] else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx in [2, 3, 4, 5] else align_left
            cell.border = cell_border

    col_widths5 = {1: 28, 2: 18, 3: 16, 4: 18, 5: 22, 6: 42, 7: 48}
    for col_idx, width in col_widths5.items():
        ws5.column_dimensions[get_column_letter(col_idx)].width = width

    # -------------------------------------------------------------
    # SHEET 6: 06_動作原理・シーケンス詳細
    # -------------------------------------------------------------
    ws6 = wb.create_sheet(title="06_動作原理・シーケンス詳細")
    ws6.views.sheetView[0].showGridLines = True

    ws6.merge_cells("A1:F1")
    ws6["A1"] = "リクエスト実行時における2層プールの動作原理と内部シーケンス"
    ws6["A1"].font = font_title
    ws6["A1"].fill = fill_title
    ws6["A1"].alignment = align_center
    ws6.row_dimensions[1].height = 38

    ws6["A2"] = "■ エンドツーエンド処理ステップ：Webリクエスト着信からDB応答・プール返却まで"
    ws6["A2"].font = font_section
    ws6.row_dimensions[2].height = 24

    seq_headers = ["Step", "実行フェーズ", "担当コンポーネント", "内部動作・処理詳細", "プール状態の変化", "例外・ボトルネック時の挙動"]
    ws6.row_dimensions[3].height = 26
    for c_idx, h in enumerate(seq_headers, 1):
        cell = ws6.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    seq_data = [
        ("Step 1", "リクエスト受信\n＆スレッド割当", "ECSフロントコンテナ\n(Undertow / Jakarta REST)", 
         "ALB経由でHTTPリクエストを受信。ワーカースレッドが割り当てられ、ビジネスロジックの実行を開始する。", 
         "IronJacamar: 待機状態\nRDS Proxy: アイドル接続を保持中", 
         "リクエスト過多時はUndertowのスレッド待機キューに積まれる。"),

        ("Step 2", "接続借用要求\n(getConnection)", "フロントIronJacamar\n(JBoss EAP 8.1)", 
         "アプリが dataSource.getConnection() を発行。IronJacamarが内部キューから利用可能なプール接続（WrappedConnection）を検索する。", 
         "空き接続あり: 即座に借用（0.001ms）\n空きなし: blocking-timeout-wait-millis まで待機", 
         "空きがなくタイムアウトした場合は IJ000453: Unable to get managed connection 例外が発生。"),

        ("Step 3", "SQLパケット送信\n(TCP / TLS)", "JDBCドライバ → RDS Proxy", 
         "WrappedConnection経由でSQLクエリを発行。コンテナ内の物理TCPソケットを通じてRDS Proxyへパケットが送信される。", 
         "コンテナ側接続: Active（使用中）\nRDS Proxyクライアント側: パケット受信", 
         "ネットワーク不通時は SocketTimeoutException が発生。"),

        ("Step 4", "多重化判定\n＆DB接続借用", "AWS RDS Proxy\n(プロキシエンジン)", 
         "RDS ProxyがSQLを解析。\n・トランザクション外単発クエリ: バックエンドDBプールから即座に空き接続を借用。\n・トランザクション中: 既存の固定（Pinned）接続を使用。\n・SET文等の状態変更あり: ピニング（固定化）を発動。", 
         "RDS Proxyバックエンド側: 接続借用（Borrow）\nDB側: クエリ処理開始", 
         "Proxy内のバックエンド接続が全使用中の場合、ConnectionBorrowTimeout まで待機。超過時はタイムアウトエラー。"),

        ("Step 5", "クエリ実行\n＆結果返却", "Amazon RDS / Aurora\n(PostgreSQL / MySQL)", 
         "DBエンジンがクエリを実行し、結果セット（ResultSet）を生成してRDS Proxy経由でコンテナへ返送する。", 
         "DBプロセス: CPU/I/Oリソース消費", 
         "スロークエリ時は query-timeout に達して中断される。"),

        ("Step 6", "バックエンド接続返却\n(Multiplexing解放)", "AWS RDS Proxy\n(プロキシエンジン)", 
         "クエリ完了（非トランザクション時）を検知すると、RDS ProxyはバックエンドDB接続を即座にプールへ返却し、他クライアントへ再割り当て可能にする。", 
         "RDS Proxyバックエンド側: 即座にIdle（返却完了）\n※これが多重化の真髄！", 
         "ピニングが発生している場合は返却されず、クライアント切断まで固定化される（性能低下要因）。"),

        ("Step 7", "接続返却\n(connection.close)", "フロントIronJacamar\n(JBoss EAP 8.1)", 
         "アプリが try-with-resources で connection.close() を実行。\nWrappedConnectionが物理ソケット切断を横取りし、接続をIronJacamarの空きキューに返却する。", 
         "IronJacamar: 接続がIdleに戻る\nコンテナ〜Proxy間TCP: 接続は維持されたまま", 
         "アプリが close() を忘れるとコネクションリークが発生する。"),

        ("Step 8", "バックグラウンド\n維持・刈り取り", "IronJacamar ＆ RDS Proxy", 
         "・IronJacamar: background-validation で死んだ接続を定期除去。idle-timeout 経過の余剰接続を破棄。\n・RDS Proxy: IdleClientTimeout 経過のゾンビ接続を切断。", 
         "プールサイズが min-pool-size に向けて自動収縮", 
         "タイムアウト整合性が崩れていると、ここで Stale Connection が発生する。")
    ]

    for r_idx, r_data in enumerate(seq_data, 4):
        ws6.row_dimensions[r_idx].height = 55
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws6.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 2, 3] else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx in [1, 2, 3] else align_left
            cell.border = cell_border

    col_widths6 = {1: 14, 2: 20, 3: 28, 4: 45, 5: 35, 6: 35}
    for col_idx, width in col_widths6.items():
        ws6.column_dimensions[get_column_letter(col_idx)].width = width

    # -------------------------------------------------------------
    # SHEET 7: 07_連携設計・サイジング・落とし穴
    # -------------------------------------------------------------
    ws7 = wb.create_sheet(title="07_連携設計・サイジング・落とし穴")
    ws7.views.sheetView[0].showGridLines = True

    ws7.merge_cells("A1:G1")
    ws7["A1"] = "2層プール連携設計・キャパシティサイジング計算モデル・運用落とし穴"
    ws7["A1"].font = font_title
    ws7["A1"].fill = fill_title
    ws7["A1"].alignment = align_center
    ws7.row_dimensions[1].height = 38

    ws7["A2"] = "■ 1. タイムアウト設定の整合性マトリクス（不整合による障害を100%防ぐルール）"
    ws7["A2"].font = font_section
    ws7.row_dimensions[2].height = 24

    timeout_headers = ["比較レイヤー", "設定パラメータ名", "推奨設定値", "関係性の絶対ルール", "ルール違反時に発生する障害事象"]
    ws7.row_dimensions[3].height = 26
    for c_idx, h in enumerate(timeout_headers, 1):
        cell = ws7.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    timeout_matrix = [
        ("アイドル切断時間", "IronJacamar: idle-timeout-minutes\nvs\nRDS Proxy: IdleClientTimeout", 
         "IronJacamar: 10分 (600秒)\nRDS Proxy: 30分 (1800秒)", 
         "【絶対遵守】\nIronJacamar (分) × 60 ＜ RDS Proxy IdleClientTimeout (秒)", 
         "【重大障害：Stale Connectionエラー】\nProxyが先にTCPを切断すると、IronJacamarは接続が死んだことを知らずプールに保持し続ける。アプリがその接続を使った瞬間に「Connection reset by peer」または「Broken pipe」でトランザクションが異常終了する。"),
        
        ("接続借用待ち時間", "IronJacamar: blocking-timeout-wait-millis\nvs\nRDS Proxy: ConnectionBorrowTimeout", 
         "IronJacamar: 5,000〜10,000ms (5〜10秒)\nRDS Proxy: 15〜30秒", 
         "【推奨ルール】\nIronJacamar待機時間 ≦ RDS Proxy借用待機時間", 
         "【スレッド枯渇障害】\nタイムアウトが長すぎると、DB過負荷時にJBossのHTTPワーカースレッドがすべて接続待ちでブロックされ、ヘルスチェック（ALB）に応答できず、タスクが次々に強制終了・再起動ループに陥る。"),
        
        ("ヘルスチェック検証", "IronJacamar: validate-on-match\nvs\nIronJacamar: background-validation", 
         "validate-on-match: false\nbackground-validation: true (30〜60秒)", 
         "【性能最適化ルール】\n貸出時の同期検証はOFFにし、非同期バックグラウンド検証のみ有効化する", 
         "【多重化性能劣化】\nvalidate-on-match=trueにすると、アプリがクエリを投げるたびに毎回「SELECT 1」等の検証クエリがProxyに飛び、Proxyの多重化処理が詰まりレイテンシが2〜5倍に悪化する。")
    ]

    for r_idx, r_data in enumerate(timeout_matrix, 4):
        ws7.row_dimensions[r_idx].height = 65
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws7.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 4] else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx in [1, 4] else align_left
            cell.border = cell_border

    ws7.cell(row=8, column=1, value="■ 2. ECSフロント／バックコンテナ ＆ RDS Proxy サイジング計算モデル").font = font_section
    ws7.row_dimensions[8].height = 24

    calc_headers = ["サイジング項目", "計算式 / 定義式", "具体例パラメータ", "算出結果", "設計根拠と安全マージン解説"]
    ws7.row_dimensions[9].height = 26
    for c_idx, h in enumerate(calc_headers, 1):
        cell = ws7.cell(row=9, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    calc_data = [
        ("① フロント側最大接続数", "Max_Front_Conn = Tasks_Front(Max) × max-pool-size(Front)", 
         "最大タスク数 = 20台\nフロント max-pool-size = 10", "200 本", 
         "フロントは短時間クエリが中心。1コンテナあたり10本で十分。20台スケールアウト時でも最大200本。"),
        
        ("② バック側最大接続数", "Max_Back_Conn = Tasks_Back(Max) × max-pool-size(Back)", 
         "最大タスク数 = 10台\nバック max-pool-size = 15", "150 本", 
         "バックはトランザクション更新・バッチ処理があるため少し多めの15本。10台スケールアウト時で最大150本。"),
        
        ("③ 全クライアント最大接続数\n(Proxyへの流入上限)", "Total_Client_Conn = Max_Front_Conn ＋ Max_Back_Conn", 
         "フロント 200本 ＋ バック 150本", "350 本\n(同時オープン)", 
         "RDS Proxyは数万のクライアント接続を保持可能。350本のクライアント接続はProxyにとって極めて軽量。"),
        
        ("④ DB本体の最大接続枠\n(RDS max_connections)", "DB_Max_Conn = DBインスタンスメモリに応じたDBパラメータ設定", 
         "Aurora PostgreSQL db.r6g.xlarge\n(メモリ 32GB、デフォルト約 5,000本)", "5,000 本\n(ハードリミット)", 
         "PostgreSQLでは1接続あたり数MB〜十数MB消費するため、物理接続上限を意識する。"),
        
        ("⑤ RDS Proxy バックエンドプール上限", "Proxy_Max_Backend = DB_Max_Conn × MaxConnectionsPercent", 
         "5,000本 × 75% (0.75)", "3,750 本\n(Proxy管理上限)", 
         "残りの 25% (1,250本) は、運用保守用接続、CloudWatchモニタリング、手動メンテ作業のために必ず確保。"),
        
        ("⑥ 実効多重化後のDB実接続数\n(ピーク稼働予測)", "Actual_DB_Conn ≒ Active_Queries_Peak ＋ Warm_Idle_Conn", 
         "アクティブクエリピーク = 50〜80並行\nアイドル維持 = 30〜50本", "80 〜 130 本\n(DB実負荷)", 
         "【驚異の多重化効果！】\nクライアントから350本の接続が来ていても、クエリ実行時のみDB接続を借用するため、DB本体の物理接続はわずか100本前後で余裕をもって処理可能！")
    ]

    for r_idx, r_data in enumerate(calc_data, 10):
        ws7.row_dimensions[r_idx].height = 42
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws7.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 4] else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx in [1, 4] else align_left
            cell.border = cell_border

    ws7.cell(row=17, column=1, value="■ 3. 現場で頻発する「三大落とし穴」とその予防・解消策").font = font_section
    ws7.row_dimensions[17].height = 24

    pitfall_headers = ["落とし穴の名称", "発生メカニズム（なぜ起きるのか？）", "システムへの悪影響", "確実な予防策・ベストプラクティス"]
    ws7.row_dimensions[18].height = 26
    for c_idx, h in enumerate(pitfall_headers, 1):
        cell = ws7.cell(row=18, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    pitfalls = [
        ("① セッションピニング爆弾\n(PostgreSQL利用時)", 
         "HibernateやPostgreSQL JDBCドライバが初期化時に「SET extra_float_digits = 3」「SET application_name = ...」等の SET文を発行したり、プロトコルレベルのPrepared Statementを使用すると、RDS Proxyが「セッション状態が汚染された」と判定してピニング（固定化）を発動する。", 
         "多重化が完全に停止し、クライアント接続とDB接続が1対1に張り付く。コンテナ数が増加した瞬間にDBの接続上限に達してシステム全停止する。", 
         "1. CloudWatchで「DatabaseConnectionsCurrentlySessionPinned」メトリクスを監視。\n2. JDBC URLに stringtype=unspecified や preferQueryMode=simple を検討。\n3. SET文はアプリから発行せず、RDS Proxyの InitQuery や DBパラメータグループで共通設定する。"),
        
        ("② コネクションリークによる\nスレッド枯渇", 
         "アプリのコーディングミスで Connection.close() が finally 句で確実に呼ばれず、IronJacamarのプールに戻らない。", 
         "コンテナ内の空き接続が徐々に減少し、最終的に blocking-timeout-wait-millis に達して全リクエストが例外（Connection pool exhausted）で落ちる。", 
         "1. try-with-resources 構文を徹底。\n2. JBoss EAP 8.1のシステムプロパティに ironjacamar.mcp=org.jboss.jca.core.connectionmanager.pool.mcp.LeakDumperManagedConnectionPool を設定し、リーク発生箇所（スタックトレース）を自動検知ログ出力する。"),
        
        ("③ フェイルオーバー時の\nゾンビ接続残留", 
         "AuroraのマルチAZフェイルオーバー発生時、古いWriterへの接続がTCPレベルで無応答（ブラックホール化）になり、アプリ側が検知できない。", 
         "アプリが古い死んだ接続を使ってクエリを投げ、SocketTimeoutまで長時間ブロックされる。", 
         "1. IronJacamar側で background-validation=true（30秒間隔）を設定。\n2. OS/JDBCレベルで TCP KeepAlive（tcpKeepAlive=true）を設定。\n3. RDS Proxyを導入していれば、Proxyがフェイルオーバーを数秒で検知して自動で新Writerに切り替えるため、根本解決となる。")
    ]

    for r_idx, r_data in enumerate(pitfalls, 19):
        ws7.row_dimensions[r_idx].height = 68
        fill = fill_stripe if r_idx % 2 == 1 else fill_white
        for c_idx, val in enumerate(r_data, 1):
            cell = ws7.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx == 1 else font_regular
            cell.fill = fill
            cell.alignment = align_center if c_idx == 1 else align_left
            cell.border = cell_border

    col_widths7 = {1: 24, 2: 36, 3: 30, 4: 20, 5: 48}
    for col_idx, width in col_widths7.items():
        ws7.column_dimensions[get_column_letter(col_idx)].width = width

    # Freeze panes on all sheets
    for ws in [ws1, ws2, ws3, ws4, ws5, ws6, ws7]:
        ws.freeze_panes = "A4"

    output_filename = "IronJacamar_RDSProxy_Comparison_Guide.xlsx"
    wb.save(output_filename)
    print(f"Successfully generated: {output_filename}")

if __name__ == "__main__":
    build_excel_guide()

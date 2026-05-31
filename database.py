import psycopg2
import psycopg2.extras

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="aws-1-ap-southeast-2.pooler.supabase.com",
            database="postgres",
            user="postgres.oyvpnbjfwnsbpsdlnyno",
            password="agungugang70", 
            port="6543",
            sslmode="require"
        )
        self.cur = self.conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    #penyewa
    def get_all_penyewa(self):
        self.cur.execute("SELECT * FROM penyewa ORDER BY nama_penyewa")
        return self.cur.fetchall()

    def tambah_penyewa(self, id_penyewa, nik, nama, telepon):
        self.cur.execute("""
            INSERT INTO penyewa (id_penyewa, nik, nama_penyewa, no_telepon)
            VALUES (%s, %s, %s, %s)
        """, (id_penyewa, nik, nama, telepon))
        self.conn.commit()

    def hapus_penyewa(self, id_penyewa):
        self.cur.execute(
            "DELETE FROM penyewa WHERE id_penyewa = %s", (id_penyewa,)
        )
        self.conn.commit()

    #Kamar
    def get_all_kamar(self):
        self.cur.execute("SELECT * FROM kamar ORDER BY id_kamar")
        return self.cur.fetchall()

    #Kontrak Sewa
    def get_all_kontrak(self):
        self.cur.execute("""
            SELECT 
                ks.id_kontrak, p.nama_penyewa, k.id_kamar,
                ks.durasi_sewa, ks.status_sewa
            FROM kontrak_sewa ks
            JOIN penyewa p ON ks.penyewa_id_penyewa = p.id_penyewa
            JOIN kamar k ON ks.kamar_id_kamar = k.id_kamar
            ORDER BY ks.status_sewa ASC
        """)
        return self.cur.fetchall()

    #Pembayaran
    def get_all_pembayaran(self):
        self.cur.execute("""
            SELECT 
                pb.id_pembayaran, p.nama_penyewa,
                k.id_kamar, pb.nominal
            FROM pembayaran pb
            JOIN kontrak_sewa ks ON pb.kontrak_sewa_id_kontrak = ks.id_kontrak
            JOIN penyewa p ON ks.penyewa_id_penyewa = p.id_penyewa
            JOIN kamar k ON ks.kamar_id_kamar = k.id_kamar
            ORDER BY pb.id_pembayaran
        """)
        return self.cur.fetchall()

    #Komplain
    def get_all_komplain(self):
        self.cur.execute("""
            SELECT 
                kp.id_komplain, p.nama_penyewa,
                k.id_kamar, kp.pesan
            FROM komplain kp
            JOIN kontrak_sewa ks ON kp.kontrak_sewa_id_kontrak = ks.id_kontrak
            JOIN penyewa p ON ks.penyewa_id_penyewa = p.id_penyewa
            JOIN kamar k ON ks.kamar_id_kamar = k.id_kamar
            ORDER BY kp.id_komplain
        """)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
from parser_types import Structure, ComplexNode, PrimitiveNode
from parser_utils import (
    clean_maybe_squashed_heading,
    clean_split_pasal_number,
    get_id,
    get_squashed_list_item,
    ignore_line,
    get_list_index_type,
    get_list_index_as_num,
    insert_penjelasan_perubahan_section_close_quotes,
    insert_penjelasan_perubahan_section_open_quotes,
    insert_perubahan_section_close_quotes,
    insert_perubahan_section_open_quotes,
    is_next_list_index_number,
    clean_law,
    roman_to_int,
    clean_maybe_list_item
)
from parser_is_start_of_x import (
    is_heading,
    is_start_of_closing,
    is_start_of_first_list_index,
    is_start_of_lembaran_number,
    is_start_of_number_with_brackets_str,
    is_start_of_number_with_brackets,
    is_start_of_number_with_right_bracket_str,
    is_start_of_number_with_right_bracket,
    is_start_of_number_with_dot_str,
    is_start_of_number_with_dot,
    is_start_of_letter_with_dot_str,
    is_start_of_letter_with_dot,
    is_start_of_list_index,
    is_start_of_list_item,
    is_start_of_list,
    is_start_of_bab_title,
    is_start_of_bab_number,
    is_start_of_bab,
    is_start_of_paragraf_title,
    is_start_of_paragraf_number,
    is_start_of_paragraf,
    is_start_of_bagian_title,
    is_start_of_bagian_number,
    is_start_of_bagian,
    is_start_of_pasal_number,
    is_start_of_pasal,
    is_start_of_agreement,
    is_start_of_penjelasan,
    is_start_of_penjelasan_ayat_str,
    is_start_of_penjelasan_huruf_str,
    is_start_of_penjelasan_pasal,
    is_start_of_penjelasan_pasal_demi_pasal,
    is_start_of_penjelasan_pasal_demi_pasal_title,
    is_start_of_penjelasan_perubahan_bab,
    is_start_of_penjelasan_perubahan_bagian,
    is_start_of_penjelasan_perubahan_pasal,
    is_start_of_penjelasan_perubahan_section,
    is_start_of_penjelasan_title,
    is_start_of_penjelasan_umum,
    is_start_of_penjelasan_umum_title,
    is_start_of_perubahan_bab,
    is_start_of_perubahan_bagian,
    is_start_of_perubahan_pasal,
    is_start_of_perubahan_section,
    is_start_of_principles,
    is_start_of_considerations,
    is_start_of_preface,
    is_start_of_unordered_list,
    is_start_of_unordered_list_index,
    is_start_of_unordered_list_item,
    is_start_of_uu_title_topic,
    is_start_of_uu_title_year_and_number,
    is_start_of_uu_title,
    is_start_of_opening,
    is_start_of_undang_undang,
    is_start_of_any,
    is_start_of_structure
)
import pytest


def test_roman_to_int():
    assert roman_to_int('VI') == 6
    assert roman_to_int('XXI') == 21
    assert roman_to_int('LIV') == 54


def test_is_heading():
    assert is_heading('BAB [0-9]+', '  BAB 23   ')
    assert not is_heading('BAB [0-9]+', 'dengan BAB 23   ')
    assert not is_heading('BAB [0-9]+', '  asdf   ')


def test_ignore_line():
    assert ignore_line('. . .')
    assert ignore_line('5 / 23')
    assert ignore_line('- 12 -')
    assert ignore_line('www.hukumonline.com')
    assert not ignore_line('Mengingat bahwa UU No. 14...')


def test_get_list_index_type():
    assert get_list_index_type('a.') == Structure.LETTER_WITH_DOT
    assert get_list_index_type('(2)') == Structure.NUMBER_WITH_BRACKETS
    assert get_list_index_type('3.') == Structure.NUMBER_WITH_DOT
    assert get_list_index_type('5)') == Structure.NUMBER_WITH_RIGHT_BRACKET
    assert get_list_index_type('Ayat (4)') == Structure.PENJELASAN_AYAT
    assert get_list_index_type('Huruf e') == Structure.PENJELASAN_HURUF
    assert get_list_index_type('Angka 17') == Structure.PENJELASAN_ANGKA

    with pytest.raises(Exception):
        get_list_index_type('cara berpikir kreatif')
        get_list_index_type('a. cara berpikir kreatif')


def test_get_list_index_as_num():
    assert get_list_index_as_num('d.') == 4
    assert get_list_index_as_num('13.') == 13
    assert get_list_index_as_num('(8)') == 8
    assert get_list_index_as_num('11)') == 11
    assert get_list_index_as_num('Ayat (8)') == 8
    assert get_list_index_as_num('Huruf d') == 4
    assert get_list_index_as_num('Angka 12') == 12
    with pytest.raises(Exception):
        get_list_index_as_num('Berhubungan dengan peraturan...')


def test_is_next_list_index_number():
    assert is_next_list_index_number('d.', 'e.') == True
    assert is_next_list_index_number('(13)', '(14)') == True
    assert is_next_list_index_number('3)', '4)') == True
    assert is_next_list_index_number('(13)', '(15)') == False
    with pytest.raises(Exception):
        is_next_list_index_number('a.', '(2)')


def test_is_start_of_first_list_index():
    assert is_start_of_first_list_index('a.') == True
    assert is_start_of_first_list_index('b.') == False

    assert is_start_of_first_list_index('1.') == True
    assert is_start_of_first_list_index('2.') == False

    assert is_start_of_first_list_index('(1)') == True
    assert is_start_of_first_list_index('(2)') == False

    assert is_start_of_first_list_index('1)') == True
    assert is_start_of_first_list_index('2)') == False

    assert is_start_of_first_list_index('Ayat (1)') == True
    assert is_start_of_first_list_index('Ayat (2)') == False

    assert is_start_of_first_list_index('Huruf a') == True
    assert is_start_of_first_list_index('Huruf b') == False

    assert is_start_of_first_list_index('Angka 1') == True
    assert is_start_of_first_list_index('Angka 2') == False

    assert is_start_of_first_list_index('dengan adanya...') == False


def test_is_start_of_number_with_brackets_str():
    assert is_start_of_number_with_brackets_str('(2)') == True
    assert is_start_of_number_with_brackets_str('b.') == False


def test_is_start_of_number_with_brackets():
    law = [
        '(1)',
        'dengan adanya...',
        '(2)',
    ]
    assert is_start_of_number_with_brackets(law, 0) == True
    assert is_start_of_number_with_brackets(law, 1) == False
    assert is_start_of_number_with_brackets(law, 2) == True


def test_is_start_of_number_with_right_bracket_str():
    assert is_start_of_number_with_right_bracket_str('2)') == True
    assert is_start_of_number_with_right_bracket_str('(2)') == False


def test_is_start_of_number_with_right_bracket():
    law = [
        '1)',
        'dengan adanya...',
        '2)',
    ]
    assert is_start_of_number_with_right_bracket(law, 0) == True
    assert is_start_of_number_with_right_bracket(law, 1) == False
    assert is_start_of_number_with_right_bracket(law, 2) == True


def test_is_start_of_number_with_dot_str():
    assert is_start_of_number_with_dot_str('2.') == True
    assert is_start_of_number_with_dot_str('b.') == False

    assert is_start_of_number_with_dot_str('2d.') == True
    assert is_start_of_number_with_dot_str('2ab.') == False


def test_is_start_of_number_with_dot():
    law = [
        '1.',
        'dengan adanya...',
        '2.',
    ]
    assert is_start_of_number_with_dot(law, 0) == True
    assert is_start_of_number_with_dot(law, 1) == False
    assert is_start_of_number_with_dot(law, 2) == True


def test_is_start_of_letter_with_dot_str():
    assert is_start_of_letter_with_dot_str('b.') == True
    assert is_start_of_letter_with_dot_str('3.') == False


def test_is_start_of_letter_with_dot():
    law = [
        'a.',
        'dengan adanya...',
        'b.',
    ]
    assert is_start_of_letter_with_dot(law, 0) == True
    assert is_start_of_letter_with_dot(law, 1) == False
    assert is_start_of_letter_with_dot(law, 2) == True


def test_is_start_of_list_index():
    law = [
        'a.',
        'dengan adanya...',
        '2.',
        'dengan adanya...',
        '(3)',
        'dengan adanya...',
        '4)',
        'Huruf g',
        'Ayat (9)',
        'Angka 5'
    ]
    assert is_start_of_list_index(law, 0) == True
    assert is_start_of_list_index(law, 1) == False
    assert is_start_of_list_index(law, 2) == True
    assert is_start_of_list_index(law, 4) == True
    assert is_start_of_list_index(law, 6) == True
    assert is_start_of_list_index(law, 7) == True
    assert is_start_of_list_index(law, 8) == True
    assert is_start_of_list_index(law, 9) == True


def test_is_start_of_list_item():
    law = [
        'Undang-Undang ini bertujuan untuk:',
        'a.',
        'menjamin hak warga negara...',
        '5)',
        'menjamin hak warga negara...',
    ]

    assert is_start_of_list_item(law, 0) == False
    assert is_start_of_list_item(law, 1) == True
    assert is_start_of_list_item(law, 2) == False
    assert is_start_of_list_item(law, 3) == True


def test_is_start_of_list():
    law = [
        'Pasal 4',
        'Undang-Undang ini bertujuan untuk:',
        'a.',
        'menjamin hak warga negara...',
        'b.',
        'mendorong partisipasi...',
    ]

    assert is_start_of_list(law, 1) == False
    assert is_start_of_list(law, 2) == True
    assert is_start_of_list(law, 4) == False


def test_is_start_of_bab_title():
    law = [
        'Untuk mewujudkan...',
        'BAB II',
        'ASAS DAN TUJUAN',
        'Pasal 1',
        'Kewajiban...',
    ]

    assert is_start_of_bab_title(law, 1) == False
    assert is_start_of_bab_title(law, 2) == True
    assert is_start_of_bab_title(law, 3) == False


def test_is_start_of_bab_number():
    law = [
        'BAB XIV',
        'KOMISI INFORMASI',
        'Pasal 23',
    ]

    assert is_start_of_bab_number(law, 0) == True
    assert is_start_of_bab_number(law, 1) == False


def test_is_start_of_bab():
    law = [
        'Ketentuan lebih lanjut...',
        'BAB XIV',
        'KOMISI INFORMASI',
        'Pasal 23',
    ]

    assert is_start_of_bab(law, 0) == False
    assert is_start_of_bab(law, 1) == True


def test_is_start_of_paragraf_title():
    law = [
        'Paragraf 2',
        'Izin Berusaha',
        'Pasal 5',
        'Badan hukum yang...',
    ]

    assert is_start_of_paragraf_title(law, 0) == False
    assert is_start_of_paragraf_title(law, 1) == True
    assert is_start_of_paragraf_title(law, 2) == False


def test_is_start_of_paragraf_number():
    law = [
        'Dalam hal kegiatan...',
        'Paragraf 2',
        'Izin Berusaha',
        'Pasal 5',
    ]

    assert is_start_of_paragraf_number(law, 0) == False
    assert is_start_of_paragraf_number(law, 1) == True
    assert is_start_of_paragraf_number(law, 2) == False


def test_is_start_of_paragraf():
    law = [
        'Ketentuan lebih lanjut...',
        'Paragraf 2',
        'Perizinan Berusaha',
        'Pasal 5',
    ]

    assert is_start_of_paragraf(law, 0) == False
    assert is_start_of_paragraf(law, 1) == True


def test_is_start_of_bagian_title():
    law = [
        'Bagian Ketiga',
        'Persyaratan Dasar',
        'Pasal 18',
        'Sesuai dengan...',
    ]

    assert is_start_of_bagian_title(law, 0) == False
    assert is_start_of_bagian_title(law, 1) == True


def test_is_start_of_bagian_number():
    law = [
        'Dalam hal kegiatan...',
        'Bagian Keempat',
        'Izin Berusaha',
        'Pasal 15',
    ]

    assert is_start_of_bagian_number(law, 0) == False
    assert is_start_of_bagian_number(law, 1) == True
    assert is_start_of_bagian_number(law, 2) == False
    # From UU 13 2003 Ketenagakerjaan [Bab XVI / Bagian 1]
    assert is_start_of_bagian_number(['Bagian Pertama'], 0) == True


def test_is_start_of_bagian():
    law = [
        'Ketentuan lebih lanjut...',
        'Bagian Ketujuh',
        'Perizinan Berusaha',
        'Pasal 5',
    ]

    assert is_start_of_bagian(law, 0) == False
    assert is_start_of_bagian(law, 1) == True


def test_is_start_of_perubahan_bagian():
    assert is_start_of_perubahan_bagian(['Bagian Kedua'], 0) == True
    assert is_start_of_perubahan_bagian(['“Bagian Pertama'], 0) == True


def test_is_start_of_penjelasan_perubahan_bagian():
    assert is_start_of_penjelasan_perubahan_bagian(['Bagian Kedua'], 0) == True
    assert is_start_of_penjelasan_perubahan_bagian(
        ['“Bagian Pertama'], 0) == True


def test_is_start_of_pasal_number():
    law = [
        'BAB IV',
        'Persyaratan Dasar',
        'Pasal 18',
        'Sesuai dengan...',
    ]

    assert is_start_of_pasal_number(law, 2) == True
    assert is_start_of_pasal_number(law, 3) == False

    assert is_start_of_pasal_number(['Pasal IV'], 0) == True
    assert is_start_of_pasal_number(['Pasal 9A'], 0) == True
    assert is_start_of_pasal_number(['Pasal IVA'], 0) == False


def test_is_start_of_pasal():
    law = [
        'Ketentuan lebih lanjut...',
        'Pasal 12',
        'Perizinan Berusaha',
    ]

    assert is_start_of_pasal(law, 0) == False
    assert is_start_of_pasal(law, 1) == True


def test_is_start_of_penjelasan_pasal():
    assert is_start_of_penjelasan_pasal(['Pasal 12'], 0) == True


def test_is_start_of_agreement():
    law = [
        'Dengan Persetujuan Bersama:',
        'DEWAN PERWAKILAN RAKYAT REPUBLIK INDONESIA',
        'dan',
        'PRESIDEN REPUBLIK INDONESIA',
        'MEMUTUSKAN:',
        'Menetapkan:',
        'UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK',
    ]

    assert is_start_of_agreement(law, 0) == True
    assert is_start_of_agreement(law, 1) == False


def test_is_start_of_principles():
    law = [
        'Mengingat:',
        'Pasal 20 Undang-Undang Dasar Negara Republik Indonesia Tahun 1945.',
    ]

    assert is_start_of_principles(law, 0) == True
    assert is_start_of_principles(law, 1) == False


def test_is_start_of_considerations():
    law = [
        'Menimbang:',
        'a. bahwa informasi...',
        'b. bahwa hak...',
        'c. bahwa keterbukaan...',
    ]

    assert is_start_of_considerations(law, 0) == True
    assert is_start_of_considerations(law, 1) == False


def test_is_start_of_preface():
    law = [
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
        'Menimbang:',
        'a. bahwa keterbukaan...',
    ]

    assert is_start_of_preface(law, 0) == True
    assert is_start_of_preface(law, 1) == False


def test_is_start_of_uu_title_topic():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_uu_title_topic(law, 3) == True
    assert is_start_of_uu_title_topic(law, 4) == False


def test_is_start_of_uu_title_year_and_number():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_uu_title_year_and_number(law, 1) == True


def test_is_start_of_uu_title():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_uu_title(law, 0) == True


def test_is_start_of_opening():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_opening(law, 0) == True


def test_is_start_of_closing():
    law = [
        'Agar setiap orang mengetahuinya, memerintahkan pengundangan Undang-Undang ini dengan  penempatannya dalam Lembaran Negara Republik Indonesia.',
        'Disahkan Di Jakarta,',
        'Pada Tanggal 25 Maret 2003',
        'PRESIDEN REPUBLIK INDONESIA,',
        'Ttd.',
        'MEGAWATI SOEKARNOPUTRI',
        'Diundangkan Di Jakarta,',
        'Pada Tanggal 25 Maret 2003',
        'SEKRETARIS NEGARA REPUBLIK INDONESIA',
        'Ttd.',
        'BAMBANG KESOWO',
        'LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN 2003 NOMOR 39',
    ]

    assert is_start_of_closing(law, 1) == True
    assert is_start_of_closing(law, 2) == False


def test_is_start_of_lembaran_number():
    law = ["LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN 2003 NOMOR 39"]
    is_start_of_lembaran_number(law, 0) == True


def test_is_start_of_undang_undang():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_undang_undang(law, 0) == True


def test_is_start_of_any():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_any(
        [Structure.UU_TITLE, Structure.LIST, Structure.BAB_TITLE],
        law,
        0
    ) == True

    assert is_start_of_any(
        [Structure.LIST, Structure.BAB_TITLE],
        law,
        0
    ) == False


def test_is_start_of_structure():
    law = [
        'BAB X',
        'GUGATAN KE PENGADILAN',
        'Pengajuan gugatan dilakukan...'
    ]

    assert is_start_of_structure(Structure.BAB_NUMBER, law, 0) == True
    assert is_start_of_structure(Structure.UU_TITLE_TOPIC, law, 0) == False


def test_get_squashed_list_item(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "y")

    assert get_squashed_list_item('nasi goreng; 3) bakmie ayam;', 0, 0) == 13
    assert get_squashed_list_item(
        'gado-gado; dan/atau j. kue lapis;', 0, 0) == 20
    # From UU 13 2003 Ketenagakerjaan [Pasal 1, list index 27]
    assert get_squashed_list_item(
        'Siang berakhir pukul 18.00. 28. 1 hari adalah waktu selama 24 jam.', 0, 0) == 28


def test_clean_maybe_list_item(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "y")

    simple = '(1) Setiap Orang berhak memperoleh Informasi Publik.'
    assert clean_maybe_list_item(simple, 0, 0) == [
        '(1)',
        'Setiap Orang berhak memperoleh Informasi Publik.',
    ]

    # From UU 14 2008 Keterbukaan Informasi Publik
    true_positive_squashed = '(1) Setiap Orang berhak dilindungi hak-hak dasar. (2) Hak-hak yang dimaksud termasuk:'
    assert clean_maybe_list_item(true_positive_squashed, 0, 0) == [
        '(1)',
        'Setiap Orang berhak dilindungi hak-hak dasar.',
        '(2)',
        'Hak-hak yang dimaksud termasuk:'
    ]

    # From UU 14 2008 Keterbukaan Informasi Publik
    false_positive_squashed = '(1) Calon anggota sebagaimana dimaksud dalam Pasal 3 ayat(2) diajukan oleh Presiden.'
    assert clean_maybe_list_item(false_positive_squashed, 0, 0) == [
        '(1)',
        'Calon anggota sebagaimana dimaksud dalam Pasal 3 ayat(2) diajukan oleh Presiden.',
    ]

    # From UU 14 2008 Keterbukaan Informasi Publik
    true_positive_squashed_first = 'Informasi yang wajib disediakan adalah: a. asas dan tujuan'
    assert clean_maybe_list_item(true_positive_squashed_first, 0, 0) == [
        'Informasi yang wajib disediakan adalah:',
        'a.',
        'asas dan tujuan',
    ]

    # From UU 14 2008 Keterbukaan Informasi Publik
    false_positive_squashed_first = 'Informasi yang wajib disediakan adalah asas dan tujuan'
    assert clean_maybe_list_item(false_positive_squashed_first, 0, 0) == [
        'Informasi yang wajib disediakan adalah asas dan tujuan',
    ]

    # From UU 13 2003 Ketenagakerjaan [Pasal 1, list index 27]
    true_positive_squashed = 'Siang berakhir pukul 18.00. 28. 1 hari adalah waktu selama 24 jam.'
    assert clean_maybe_list_item(true_positive_squashed, 0, 0) == [
        'Siang berakhir pukul 18.00.',
        '28.',
        '1 hari adalah waktu selama 24 jam.'
    ]

    # From UU 13 2003 Ketenagakerjaan [Pasal 79, list index 1]
    true_positive_squashed_multiple_whitespace = 'Pengusaha wajib memberi cuti kepada pekerja.  (2) Waktu istirahat dan cuti sebagaimana'
    assert clean_maybe_list_item(true_positive_squashed_multiple_whitespace, 0, 0) == [
        'Pengusaha wajib memberi cuti kepada pekerja.',
        '(2)',
        'Waktu istirahat dan cuti sebagaimana'
    ]

    # From UU 13 2003 Ketenagakerjaan [Pasal 79, list index 1]
    true_positive_multiple_list_index_structures = '(1) Pengusaha wajib memberi waktu istirahat dan cuti kepada pekerja/buruh.  (2) Waktu istirahat dan cuti sebagaimana dimaksud dalam ayat (1), meliputi:  a. istirahat antara jam kerja, sekurang'
    assert clean_maybe_list_item(true_positive_multiple_list_index_structures, 0, 0) == [
        '(1)',
        'Pengusaha wajib memberi waktu istirahat dan cuti kepada pekerja/buruh.',
        '(2)',
        'Waktu istirahat dan cuti sebagaimana dimaksud dalam ayat (1), meliputi:',
        'a.',
        'istirahat antara jam kerja, sekurang',
    ]

    # From UU 13 2003 Ketenagakerjaan [Penjelasan, I. Umum]
    true_positive_unordered_list_squashed = '− Kebebasan Berserikat;  − Diskriminasi; '
    assert clean_maybe_list_item(true_positive_unordered_list_squashed, 0, 0) == [
        '−',
        'Kebebasan Berserikat;',
        '−',
        'Diskriminasi;',
    ]

    # From UU 13 2003 Ketenagakerjaan [Penjelasan, II. Pasal demi Pasal, Pasal 4, Huruf b/c]
    true_positive_penjelasan_huruf = 'Penempatan tenaga kerja diatur agar mengisi kebutuhan seluruh daerah.  Huruf c'
    assert clean_maybe_list_item(true_positive_penjelasan_huruf, 0, 0) == [
        'Penempatan tenaga kerja diatur agar mengisi kebutuhan seluruh daerah.',
        'Huruf c'
    ]

    true_positive_penjelasan_ayat = 'Penempatan tenaga kerja diatur agar mengisi kebutuhan seluruh daerah.  Ayat (12)'
    assert clean_maybe_list_item(true_positive_penjelasan_ayat, 0, 0) == [
        'Penempatan tenaga kerja diatur agar mengisi kebutuhan seluruh daerah.',
        'Ayat (12)'
    ]


def test_clean_maybe_squashed_heading(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "y")

    line = "Di antara Bab V dan Bab VI disisipkan satu bab: “Pasal 5A"
    assert clean_maybe_squashed_heading(line, 0, 0) == [
        "Di antara Bab V dan Bab VI disisipkan satu bab:",
        "“Pasal 5A"
    ]

    line = "Di antara Bab V dan Bab VI disisipkan satu bab: Pasal II"
    assert clean_maybe_squashed_heading(line, 0, 0) == [
        "Di antara Bab V dan Bab VI disisipkan satu bab:",
        "Pasal II"
    ]

    line = "Di antara Bab V dan Bab VI disisipkan satu bab: BAB XV"
    assert clean_maybe_squashed_heading(line, 0, 0) == [
        "Di antara Bab V dan Bab VI disisipkan satu bab:",
        "BAB XV"
    ]

    line = "Di antara Bab V dan Bab VI disisipkan satu bab: “BAB VA"
    assert clean_maybe_squashed_heading(line, 0, 0) == [
        "Di antara Bab V dan Bab VI disisipkan satu bab:",
        "“BAB VA"
    ]

    line = "Demikian saja. PASAL DEMI PASAL"
    assert clean_maybe_squashed_heading(line, 0, 0) == [
        "Demikian saja.",
        "PASAL DEMI PASAL",
    ]


def test_get_id():
    bab_node = ComplexNode(type=Structure.BAB)
    bab_node.add_child(PrimitiveNode(
        type=Structure.BAB_NUMBER, text="BAB III"))
    bab_node.add_child(PrimitiveNode(
        type=Structure.BAB_TITLE, text="PEMULIHAN EKONOMI"))
    assert get_id(bab_node) == 'bab-3'

    bagian_node = ComplexNode(type=Structure.BAGIAN)
    bagian_node.add_child(PrimitiveNode(
        type=Structure.BAGIAN_NUMBER, text="Bagian Pertama"))
    bagian_node.add_child(PrimitiveNode(
        type=Structure.BAGIAN_TITLE, text="Jasa Kurir"))

    bab_node.add_child(bagian_node)
    assert get_id(bagian_node) == 'bab-3-bagian-1'

    bagian_node_2 = ComplexNode(type=Structure.BAGIAN)
    bagian_node_2.add_child(PrimitiveNode(
        type=Structure.BAGIAN_NUMBER, text="Bagian Kedelapan"))
    bagian_node_2.add_child(PrimitiveNode(
        type=Structure.BAGIAN_TITLE, text="Jasa Ojek Online"))

    bab_node.add_child(bagian_node_2)
    assert get_id(bagian_node_2) == 'bab-3-bagian-8'

    bagian_node_3 = ComplexNode(type=Structure.BAGIAN)
    bagian_node_3.add_child(PrimitiveNode(
        type=Structure.BAGIAN_NUMBER, text="Bagian Kedua Belas"))
    bagian_node_3.add_child(PrimitiveNode(
        type=Structure.BAGIAN_TITLE, text="Jasa Ojek Online"))

    bab_node.add_child(bagian_node_3)
    assert get_id(bagian_node_3) == 'bab-3-bagian-12'

    pasal_node = ComplexNode(type=Structure.PASAL)
    bab_node.add_child(pasal_node)
    pasal_node.add_child(PrimitiveNode(
        type=Structure.PASAL_NUMBER, text="Pasal 12"))
    assert get_id(pasal_node) == 'pasal-12'


def test_is_start_of_penjelasan():
    law = [
        'PENJELASAN',
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 13 TAHUN 2003',
        'TENTANG',
        'KETENAGAKERJAA',
    ]
    assert is_start_of_penjelasan(law, 0) == True


def test_is_start_of_penjelasan_title():
    law = [
        'PENJELASAN',
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 13 TAHUN 2003',
        'TENTANG',
        'KETENAGAKERJAA',
    ]
    assert is_start_of_penjelasan_title(law, 0) == True

    law = [
        'PENJELASAN',
        'ATAS',
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 13 TAHUN 2003',
        'TENTANG',
        'KETENAGAKERJAA',
    ]
    assert is_start_of_penjelasan_title(law, 0) == True


def test_is_start_of_unordered_list_index():
    # From UU 13 2003 Ketenagakerjaan [Penjelasan, I. Umum]
    law = ['− Ordonansi tentang Pengerahan Orang Indonesia Untuk Melakukan Pekerjaan Di Luar Indonesia']
    assert is_start_of_unordered_list_index(law, 0) == True


def test_is_start_of_unordered_list_item():
    law = ['− Ordonansi tentang Pengerahan Orang Indonesia Untuk Melakukan Pekerjaan Di Luar Indonesia']
    assert is_start_of_unordered_list_item(law, 0) == True


def test_is_start_of_unordered_list():
    law = ['− Ordonansi tentang Pengerahan Orang Indonesia Untuk Melakukan Pekerjaan Di Luar Indonesia']
    assert is_start_of_unordered_list(law, 0) == True


def test_is_start_of_penjelasan_umum():
    law = [
        'I. UMUM',
        'Pembangunan ketenagakerjaan sebagai bagian integral...',
    ]
    assert is_start_of_penjelasan_umum(law, 0) == True


def test_is_start_of_penjelasan_umum_title():
    law = [
        'I. UMUM',
        'Pembangunan ketenagakerjaan sebagai bagian integral...',
    ]
    assert is_start_of_penjelasan_umum_title(law, 0) == True


def test_is_start_of_penjelasan_huruf_str():
    assert is_start_of_penjelasan_huruf_str('Huruf e') == True
    assert is_start_of_penjelasan_huruf_str('Huruf e.') == False
    assert is_start_of_penjelasan_huruf_str('e.') == False
    assert is_start_of_penjelasan_huruf_str(
        'Yang dimaksud dengan Huruf e') == False


def test_is_start_of_penjelasan_ayat_str():
    assert is_start_of_penjelasan_ayat_str('Ayat (2)') == True
    assert is_start_of_penjelasan_ayat_str('(2)') == False
    assert is_start_of_penjelasan_ayat_str(
        'Yang dimaksud dengan Ayat (2)') == False


def test_is_start_of_penjelasan_pasal_demi_pasal():
    assert is_start_of_penjelasan_pasal_demi_pasal(
        ['II. PASAL DEMI PASAL'], 0) == True
    assert is_start_of_penjelasan_pasal_demi_pasal(
        ['I. PASAL DEMI PASAL'], 0) == False


def test_is_start_of_penjelasan_pasal_demi_pasal_title():
    assert is_start_of_penjelasan_pasal_demi_pasal_title(
        ['II. PASAL DEMI PASAL'], 0) == True
    assert is_start_of_penjelasan_pasal_demi_pasal_title(
        ['I. PASAL DEMI PASAL'], 0) == False

    # From UU 1 1974 Perkawinan [Penjelasan]
    assert is_start_of_penjelasan_pasal_demi_pasal_title(
        ['PASAL DEMI PASAL'], 0) == True
    assert is_start_of_penjelasan_pasal_demi_pasal_title(
        ['Arti PASAL DEMI PASAL adalah'], 0) == False


def test_is_start_of_perubahan_section():
    assert is_start_of_perubahan_section(['“Pasal 3'], 0) == True
    assert is_start_of_perubahan_section(['Pasal 3'], 0) == False


def test_is_start_of_penjelasan_perubahan_section():
    assert is_start_of_penjelasan_perubahan_section(['“BAB III'], 0) == True
    assert is_start_of_penjelasan_perubahan_section(['BAB III'], 0) == False


def test_is_start_of_penjelasan_perubahan_pasal():
    assert is_start_of_penjelasan_perubahan_pasal(['“Pasal 3'], 0) == True
    assert is_start_of_penjelasan_perubahan_pasal(['Pasal 3'], 0) == True


def test_is_start_of_perubahan_pasal():
    assert is_start_of_perubahan_pasal(['“Pasal 3'], 0) == True
    assert is_start_of_perubahan_pasal(['Pasal 3'], 0) == True


def test_is_start_of_perubahan_bab():
    assert is_start_of_perubahan_bab(['“BAB III'], 0) == True
    assert is_start_of_perubahan_bab(['BAB III'], 0) == True


def test_is_start_of_penjelasan_perubahan_bab():
    assert is_start_of_penjelasan_perubahan_bab(['“BAB III'], 0) == True
    assert is_start_of_penjelasan_perubahan_bab(['BAB III'], 0) == True


def test_insert_perubahan_section_open_quotes(monkeypatch):
    law = [
        'Pasal I'
    ]
    assert insert_perubahan_section_open_quotes(law) == law

    law = [
        'Pasal 5',
        'BAB X',
        'abcdefg',
        'Bagian Ketujuh',
    ]
    new_law = [
        '“Pasal 5',
        '“BAB X',
        'abcdefg',
        '“Bagian Ketujuh',
    ]
    monkeypatch.setattr('builtins.input', lambda: "y")
    assert insert_perubahan_section_open_quotes(law) == new_law


def test_insert_perubahan_section_close_quotes(monkeypatch):
    law = [
        '“Pasal 5',
        'Hari rabu dinyatakan hari libur”',
        '“Pasal 6',
        'Hari kamis dinyatakan hari libur”',
    ]

    assert insert_perubahan_section_close_quotes(law) == law

    law = [
        '“Pasal 5',
        'Hari rabu dinyatakan hari libur',
        '“Pasal 6',
        'Hari kamis dinyatakan hari libur”',
    ]
    new_law = [
        '“Pasal 5',
        'Hari rabu dinyatakan hari libur”',
        '“Pasal 6',
        'Hari kamis dinyatakan hari libur”',
    ]
    monkeypatch.setattr('builtins.input', lambda: "1")
    assert insert_perubahan_section_close_quotes(law) == new_law


def test_insert_penjelasan_perubahan_section_open_quotes():
    law = [
        '“Pasal 5',
        'Hari rabu dinyatakan hari libur”',
        '“Pasal 6',
        'Hari kamis dinyatakan hari libur”',
        'PENJELASAN',
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'II. PASAL DEMI PASAL',
        'Pasal 5',
        'Cukup jelas.',
        'Pasal 6',
        'Cukup jelas.'
    ]
    new_law = [
        '“Pasal 5',
        'Hari rabu dinyatakan hari libur”',
        '“Pasal 6',
        'Hari kamis dinyatakan hari libur”',
        'PENJELASAN',
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'II. PASAL DEMI PASAL',
        '“Pasal 5',
        'Cukup jelas.',
        '“Pasal 6',
        'Cukup jelas.'
    ]
    assert insert_penjelasan_perubahan_section_open_quotes(law) == new_law


def test_insert_penjelasan_perubahan_section_close_quotes(monkeypatch):
    law = [
        '“Pasal 5',
        'Hari rabu dinyatakan hari libur”',
        '“Pasal 6',
        'Hari kamis dinyatakan hari libur”',
        'PENJELASAN',
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'II. PASAL DEMI PASAL',
        'Pasal I',
        'Angka 1',
        '“Pasal 5',
        'Cukup jelas.',
        'Angka 2',
        '“Pasal 6',
        'Cukup jelas.',
        'Angka 3',
        'Cukup jelas.'
    ]
    new_law = [
        '“Pasal 5',
        'Hari rabu dinyatakan hari libur”',
        '“Pasal 6',
        'Hari kamis dinyatakan hari libur”',
        'PENJELASAN',
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'II. PASAL DEMI PASAL',
        'Pasal I',
        'Angka 1',
        '“Pasal 5',
        'Cukup jelas.”',
        'Angka 2',
        '“Pasal 6',
        'Cukup jelas.”',
        'Angka 3',
        'Cukup jelas.'
    ]

    monkeypatch.setattr('builtins.input', lambda: "y")
    assert insert_penjelasan_perubahan_section_close_quotes(law) == new_law


def test_clean_split_pasal_number():
    law = [
        'Pasal 39 B',
        'Pasal 39    B',
        '“Pasal 39 B',
        'Pasal II',
        'Pasal 54',
    ]
    clean_law = [
        'Pasal 39B',
        'Pasal 39B',
        '“Pasal 39B',
        'Pasal II',
        'Pasal 54',
    ]
    assert clean_split_pasal_number(law) == clean_law

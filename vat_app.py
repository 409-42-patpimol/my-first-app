import streamlit as st
st.title("🛒แอปพลิเคชั่นคำนวณราคาสินค้ารวม VAT 7%")
price = st.number_input("กรอกราคาสินค้า (บาท):", value=0.0)
st.header(f"• ภาษีมูลค่าเพิ่ม (VAT 7%): **{vat:.2f}** บาท")
net_price = price - vat
vat = price * 0.07
price = st.number_input("กรอกราคาสินค้า (บาท):", value=0.0)
st.divider()
st.write("นางสาวพัตรพิมล เงินสุข ม.4/9 เลขที่42")

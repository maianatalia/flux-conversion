import sqlite3
import math
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

conn = sqlite3.connect('banco.sqlite')
pi = math.pi
# pi = 3.14
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
A = 2.5E-04
N = 1.4
alpha = 4.6
rest_freq_co_10 = 115.271E9
rest_freq_co_32 = 345.796E9


def main():
    # CO[3-2] (345.796 GHz rest frame)
    # CO[1-0] (115.271 GHz rest frame)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flux_conversion')
    result = cursor.fetchall()
    for row in result:
        radius = row[5]*10**3   # radius in parsec
        m_gas = ((pi*(radius)**2)*(row[4]/(A*pi*(row[5])**2))**(1/N))
        L_co = m_gas / alpha
        flux_conversion_id = row[0]
        m_gas_result = m_gas*10**-9
        L_co_result = L_co * 10 ** -9
        D = cosmo.luminosity_distance(row[1])/(1 * u.megaparsec)
        D_float = float(D)
        flux_10 = (L_co*(1+row[1])*(rest_freq_co_10)**2)/(3.25E7*D_float**2)
        flux_32 = (L_co*(1+row[1])*(rest_freq_co_32)**2)/(3.25E7*D_float**2)
        print m_gas_result, L_co_result
        # cursor.execute('''INSERT INTO parcial_results(flux_conversion_id, m_gas_sfrhalpha24, l_co_sfrhalpha24, flux_10_sfrhalpha24, flux_32_sfrhalpha24)
        #           VALUES (?,?,?,?,?)''', (flux_conversion_id, m_gas_result, L_co_result, flux_10, flux_32))
        print "{} foi inserido".format(row[0])
    conn.commit()



main()
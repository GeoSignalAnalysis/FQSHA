import math
import numpy as np
import os
from scipy.stats import norm, invgauss
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from src.FQSHA_Functions import TruncatedGR, CHGaussPoiss, CHGaussBPT
from src.FQSHA_Functions import kin2coeff, coeff2mag, conflate_pdfs
# from scipy.integrate import trapezoid
from numpy import trapezoid


def momentbudget(faults, Zeta, Khi, Siggma, ProjFol, logical_nan, logical_nan_sdmag):
    # Constants
    d = 9.1
    c = 1.5
    dMMO = Siggma

    # Initialize output array
    output_Mmax_sigmaMmax = np.empty((0, 2), float)

    for fault_name, values in faults.items():
        try:
            # ===== PARAMETER INITIALIZATION =====
            # Handle ShearModulus
            if 'ShearModulus' in values and values['ShearModulus'] is None:
                print(f"Fault {fault_name} has a 'NaN' ShearModulus value.")
                values['ShearModulus'] = 3 * 1e10
            else:
                values['ShearModulus'] = float(values['ShearModulus']) * 1e10

            # Handle StrainDrop
            if 'StrainDrop' in values and values['StrainDrop'] is None:
                values['StrainDrop'] = 3 * 1e-5
            else:
                values['StrainDrop'] = float(values['StrainDrop']) * 1e-5

            # Handle Last_eq_time
            if 'Last_eq_time' in values:
                if values['Last_eq_time'] is None or str(values['Last_eq_time']).lower() == 'nan' or values[
                    'Last_eq_time'] == '':
                    if logical_nan:
                        values['Last_eq_time'] = float('nan')
                else:
                    values['Last_eq_time'] = float(values['Last_eq_time'])

            # Handle sdmag
            if 'sdmag' in values:
                if values['sdmag'] is None or str(values['sdmag']).lower() == 'nan' or values['sdmag'] == '':
                    if logical_nan_sdmag:
                        values['sdmag'] = float('nan')
                else:
                    values['sdmag'] = float(values['sdmag'])

            # ===== BASIC PARAMETERS =====
            ScR = values['ScR']
            Length = float(values['Length']) * 1000
            Dip = math.radians(float(values['Dip']))
            sine_Dip = math.sin(Dip)
            upperSeismoDepth = float(values['upperSeismoDepth'])
            lowerSeismoDepth = float(values['lowerSeismoDepth'])
            Seismogenic_thickness = (lowerSeismoDepth - upperSeismoDepth) * 1000
            Width = Seismogenic_thickness / sine_Dip
            Slipmin = float(values['SRmin'])
            Slipmax = float(values['SRmax'])
            V = (Slipmin + Slipmax) / 2000
            dV = V - (Slipmin / 1000)
            mag = float(values['Mobs']) if 'Mobs' in values and not math.isnan(values['Mobs']) else float('nan')
            sdmag = float(values['sdMobs']) if 'sdMobs' in values and not math.isnan(values['sdMobs']) else float('nan')
            SCC = float(values['SCC'])
            yfc = float(values['year_for_calculations'])

            # Calculate Telap
            Telap = yfc - float(values['Last_eq_time']) if not math.isnan(values['Last_eq_time']) else float('nan')

            # ===== MAGNITUDE CALCULATIONS =====
            mu = values['ShearModulus']
            straindrop = values['StrainDrop']
            MMO = (1 / c) * (math.log10(straindrop * mu * Length ** 2 * Width) - d)

            # Get coefficients from scaling relationship
            coeff, ARtable = kin2coeff(ScR)
            MRLD, MRA, dMRLD, dMRA, MAR, ar_coeff, LAR, legends_Mw = coeff2mag(
                ScR, coeff, Length, Width, ARtable, mu, straindrop)

            M = np.array([MMO, MAR, MRLD, MRA])
            M = np.round(M * 100) / 100
            dM1 = np.array([dMMO, ar_coeff[2], dMRLD, dMRA])
            dM1 = np.round(dM1 * 100) / 100

            # Remove NaN values
            M = M[~np.isnan(M)]
            dM1 = dM1[~np.isnan(dM1)]
            Mmean = np.mean(M)

            # ===== MAGNITUDE CONFLATION =====
            flag_mobs = 0
            if not math.isnan(mag):
                if mag < Mmean:
                    flag_mobs = 1
                    if abs(mag - Mmean) < Zeta:
                        sdmag = sdmag
                    elif abs(mag - Mmean) > Zeta:
                        sdmag = np.mean(dM1) + Khi * abs(mag - Mmean)
                else:
                    flag_mobs = 1
                    if abs(mag - Mmean) > Zeta:
                        print('Warning: Please consider revising the geometry parameters.')

            M = np.concatenate(([MMO, MAR, MRLD, MRA], [mag] if not math.isnan(mag) else []))
            dM = np.concatenate(([dMMO, ar_coeff[2], dMRLD, dMRA], [sdmag] if not math.isnan(mag) else []))
            dM = np.round(np.array(dM) * 100) / 100

            # Determine magnitude range
            min_val = np.floor(np.min(M - dM))
            max_val = np.ceil(np.max(M + dM))
            x_range_of_mag = np.arange(min_val, max_val + 0.01, 0.01)

            # Calculate PDFs
            pdf_magnitudes = []
            for k in range(len(M)):
                pdf_magnitudes.append(norm.pdf(x_range_of_mag, M[k], dM[k]))
            pdf_magnitudes = np.array(pdf_magnitudes)
            pdf_magnitudes /= np.tile(np.max(pdf_magnitudes, axis=1)[:, np.newaxis], (1, pdf_magnitudes.shape[1]))

            # Summed distribution
            if LAR >= Length:
                pdf_magnitudes = np.delete(pdf_magnitudes, 1, axis=0)
            summed_pdf_magnitudes = np.sum(pdf_magnitudes, axis=0)

            # Conflated distribution
            conflated = conflate_pdfs(x_range_of_mag, pdf_magnitudes)

            if flag_mobs == 1 and not math.isnan(mag):
                pp = norm.pdf(x_range_of_mag, mag, sdmag)
                pdf_magnitudes[-1] = pdf_magnitudes[-1] * (trapezoid(pp) / trapezoid(pdf_magnitudes[-1]))

            # Calculate weighted mean and std
            weighted_mean = np.average(x_range_of_mag, weights=summed_pdf_magnitudes)
            weighted_std = np.sqrt(np.average((x_range_of_mag - weighted_mean) ** 2, weights=summed_pdf_magnitudes))

            Mmax = weighted_mean
            sigma_Mmax = weighted_std
            Mmax = round(Mmax * 10) / 10
            sigma_Mmax = round(sigma_Mmax * 10) / 10
            print(f"Mmax: {Mmax}, sigma_Mmax: {sigma_Mmax}")

            # ===== Tmean CALCULATION =====
            try:
                L_forTmean = Length if LAR >= Length else LAR
                numerator = 10 ** (d + c * Mmax)
                denominator = mu * V * L_forTmean * Width
                Tmean = np.round(numerator / denominator * (1 / SCC))

                if Tmean <= 0:
                    raise ValueError("Non-positive Tmean")

                Tmean = float(Tmean)
                MomentRate = float(10 ** (d + c * Mmax) / Tmean)

                # Store in output array
                output_Mmax_sigmaMmax = np.vstack([output_Mmax_sigmaMmax, [Mmax, sigma_Mmax]])

            except (ZeroDivisionError, ValueError) as e:
                print(f"Warning: Could not calculate Tmean for {fault_name}: {str(e)}")
                Tmean = float('nan')
                MomentRate = float('nan')

            # ===== PLOTTING =====
            plt.style.use('dark_background')
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111)

            # Plot individual PDFs
            count_pdf = 0
            ax.plot(x_range_of_mag, pdf_magnitudes[count_pdf, :], 'b-', linewidth=1.2, label='MMo')
            count_pdf += 1

            if LAR < Length:
                ax.plot(x_range_of_mag, pdf_magnitudes[count_pdf, :], 'g-', linewidth=1.4, label='MAR')
                count_pdf += 1

            ax.plot(x_range_of_mag, pdf_magnitudes[count_pdf, :], 'r-', linewidth=1.0, label=legends_Mw[0])
            count_pdf += 1
            ax.plot(x_range_of_mag, pdf_magnitudes[count_pdf, :], 'c-', linewidth=1.2, label=legends_Mw[1])
            count_pdf += 1

            if not math.isnan(mag):
                ax.plot(x_range_of_mag, pdf_magnitudes[count_pdf, :], 'm-', linewidth=1.2, label='MObs')

            # Plot combined PDFs
            ax.plot(x_range_of_mag, summed_pdf_magnitudes, '--', color='gray', linewidth=1.2, label='SEM')
            ax.plot(x_range_of_mag, conflated, 'gold', linewidth=2.0, label='CoP')

            # Mark Mmax
            Mmax1 = x_range_of_mag[np.argmax(conflated)]
            ax.stem(Mmax1, np.max(conflated), linefmt='w-', markerfmt='wo', basefmt=' ')

            # Create legend
            legend_entries = ['MMo']
            if LAR < Length:
                legend_entries.append('MAR')
            legend_entries.extend(legends_Mw)
            if not math.isnan(mag):
                legend_entries.append('MObs')
            legend_entries.extend(['SEM', 'CoP', 'Mmax'])

            ax.legend(legend_entries)
            ax.fill_between(x_range_of_mag, 0, conflated, color='gold', alpha=0.25)
            ax.set_xlabel('Magnitude', fontsize=14)
            ax.set_ylabel('Probability density function', fontsize=14)
            ax.set_title(fault_name)
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=5)
            plt.tight_layout()

            # Save figure
            fig_dir = os.path.join(ProjFol, "Figures") if ProjFol else "output_files/Figures"
            os.makedirs(fig_dir, exist_ok=True)
            fig_path = os.path.join(fig_dir, f'Conflation_of_PDFs_{fault_name}.pdf')
            plt.savefig(fig_path, dpi=1200, bbox_inches='tight')
            plt.show()

            # ===== STORE RESULTS =====
            values.update({
                'Mmax': float(Mmax),
                'sdMmax': float(sigma_Mmax),
                'Tmean': Tmean,
                'Telap': float(Telap) if not math.isnan(Telap) else float('nan'),
                'MomentRate': MomentRate,
                'L_forTmean': float(L_forTmean),
                'Width': float(Width),
                'V': float(V)
            })

            print(f"Fault: {fault_name}, Tmean: {values['Tmean']}, SCC: {SCC}, "
                  f"V: {V}, L_forTmean: {L_forTmean / 1000}, Width: {Width}")

        except Exception as e:
            print(f"Error processing fault {fault_name}: {str(e)}")
            values.update({
                'Mmax': float('nan'),
                'sdMmax': float('nan'),
                'Tmean': float('nan'),
                'Telap': float('nan'),
                'MomentRate': float('nan'),
                'L_forTmean': float('nan'),
                'Width': float('nan'),
                'V': float('nan')
            })
            continue

    return faults





def sactivityrate(faults, Fault_behaviour, w, bin, ProjFol):
    d = 9.1
    c = 1.5
    field_names = list(faults.keys())
    nfault = len(field_names)

    # Initialize arrays with NaN as default
    id = np.full(nfault, np.nan)
    mag = np.full(nfault, np.nan)
    sdmag = np.full(nfault, np.nan)
    Tmean = np.full(nfault, np.nan)
    alpha_val = np.full(nfault, np.nan)
    Telapsed = []
    Morate_input = np.full(nfault, np.nan)
    fault_name = []
    idgr = np.full(nfault, np.nan)
    mt = np.full(nfault, np.nan)
    b = np.full(nfault, np.nan)

    # Iterate over each fault with error handling
    for i, field_name in enumerate(field_names):
        try:
            sub_struct = faults[field_name]
            id[i] = float(sub_struct.get('id', np.nan))
            mag[i] = float(sub_struct.get('Mmax', np.nan))
            sdmag[i] = float(sub_struct.get('sdMmax', np.nan))
            Morate_input[i] = float(sub_struct.get('MomentRate', np.nan))
            Tmean[i] = float(sub_struct.get('Tmean', np.nan))
            Telapsed.append(float(faults[field_name].get('Telap', np.nan)))
            alpha_val[i] = float(sub_struct.get('CV', np.nan))
            idgr[i] = float(sub_struct.get('id', np.nan))
            mt[i] = float(sub_struct.get('Mmin', np.nan))
            b[i] = float(sub_struct.get('b-value', np.nan))
            fault_name.append(field_name)
        except (ValueError, TypeError) as e:
            print(f"Error processing fault {field_name}: {str(e)}")
            continue

    # Calculate moment rates with validation
    valid_mask = ~np.isnan(mag) & ~np.isnan(Tmean)
    Morate_fromTmean = np.full(nfault, np.nan)
    Morate_fromTmean[valid_mask] = 10 ** (c * mag[valid_mask] + d) / Tmean[valid_mask]

    valid_mask = ~np.isnan(mag) & ~np.isnan(Morate_input)
    Tmean_fromMorate = np.full(nfault, np.nan)
    Tmean_fromMorate[valid_mask] = np.round(10 ** (c * mag[valid_mask] + d) / Morate_input[valid_mask]).astype(int)

    Morate = np.where(~np.isnan(Morate_fromTmean), Morate_fromTmean, Morate_input)

    # Compare moment rates
    for i in range(nfault):
        if not np.isnan(Morate_fromTmean[i]) and not np.isnan(Morate_input[i]):
            if not np.isclose(Morate_fromTmean[i], Morate_input[i], rtol=0.01):
                print(f"Warning: Mo rate computed using M and Tmean for fault #{i} is {Morate_fromTmean[i]:.4e}, "
                      f"different from input {Morate_input[i]:.4e}")

    Hbpt = np.zeros(nfault)
    Hpois = np.zeros(nfault)

    for i in range(nfault):
        try:
            # Skip if missing essential values
            if np.isnan(mag[i]) or np.isnan(sdmag[i]) or np.isnan(Morate_input[i]):
                continue

            # Validate and adjust magnitude range
            if sdmag[i] <= 0:
                print(f"Warning: Invalid sdmag ({sdmag[i]}) for fault {i}, using default bin size")
                sdmag[i] = bin

            start = mag[i] - sdmag[i]
            stop = mag[i] + sdmag[i] + bin

            if start >= stop:
                print(f"Warning: Invalid range for fault {i}, adjusting range")
                start = mag[i] - bin
                stop = mag[i] + bin + 0.1

            magnitude_range = np.arange(start, stop, bin)

            # Calculate moment and PDF
            M = 10 ** (c * magnitude_range + d)
            pdf_mag = norm.pdf(magnitude_range, mag[i], sdmag[i])
            total_moment = np.sum(pdf_mag * M)

            if total_moment <= 0:
                print(f"Warning: Non-positive total moment for fault {i}")
                continue

            ratio = Morate_input[i] / total_moment
            balanced_pdf_moment = ratio * pdf_mag
            CumRateMmin = np.sum(balanced_pdf_moment)

            if CumRateMmin <= 0:
                print(f"Warning: Non-positive CumRateMmin for fault {i}")
                continue

            Tm = 1 / CumRateMmin

            # Handle Telap calculations
            Telap = Telapsed[i] if i < len(Telapsed) else np.nan
            if not np.isnan(Telap):
                if Telap > 10 * Tm:
                    Telap = 10 * Tm
                    print(f'Warning: Telap for fault id {id[i]} adjusted to 10*Tm')

                alpha = alpha_val[i] if not np.isnan(alpha_val[i]) else 0.5  # Default alpha

                try:
                    scale = Tm / (alpha ** 2)
                    Hbpt_a1 = invgauss.cdf((Telap + w) / scale, mu=Tm / scale)
                    Hbpt_a2 = invgauss.cdf(Telap / scale, mu=Tm / scale)
                    Hbpt[i] = min((Hbpt_a1 - Hbpt_a2) / (1 - Hbpt_a2), 1.0)
                except Exception as e:
                    print(f"Error calculating Hbpt for fault {i}: {str(e)}")
                    Hbpt[i] = 0

            # Poisson probability
            try:
                Hpois[i] = min(1 - np.exp(-w / Tm), 1.0) if Tm > 0 else 0
            except:
                Hpois[i] = 0

        except Exception as e:
            print(f"Error processing fault {i}: {str(e)}")
            continue

    # Handle different fault behaviors with validation
    try:
        if Fault_behaviour == "Characteristic Gaussian":
            if any(not np.isnan(t) for t in Telapsed):
                CHGaussBPT(faults, c, d, ProjFol, fault_name, mag, sdmag, Tmean, Morate, id, nfault, w, Hbpt, bin)
            else:
                CHGaussPoiss(faults, c, d, ProjFol, fault_name, mag, sdmag, Morate, id, nfault, w, Hpois, bin)
        elif Fault_behaviour == "Truncated Gutenberg Richter":
            TruncatedGR(faults, c, d, ProjFol, fault_name, mag, mt, Morate, id, nfault, bin, b)
        else:
            print(f"Warning: Unknown fault behavior '{Fault_behaviour}'")
    except Exception as e:
        print(f"Error in fault behavior processing: {str(e)}")

    return faults
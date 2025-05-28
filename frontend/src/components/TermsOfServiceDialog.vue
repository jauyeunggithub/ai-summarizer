<template>
  <div class="modal fade modal-xl" tabindex="-1" ref="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Terms Of Service and Privacy Policy - Online AI Summarizer</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body m-0 p-3 overflow-auto" :style="{ height: '70vh' }">
          <h1>Terms of Service</h1>
          <p><strong>Effective Date:</strong> [Insert Date]</p>

          <p>
            Welcome to [Your AI Summarizer Name] ("Service", "we", "us", or "our"). By accessing or
            using our AI summarization services (the "Services"), you agree to be bound by these
            Terms of Service ("Terms"). If you do not agree to these Terms, please do not use our
            Services.
          </p>

          <h2>1. Use of Service</h2>
          <p>
            You may use the Service only in compliance with these Terms and all applicable laws. The
            Service allows users to input text or documents to generate summaries using artificial
            intelligence.
          </p>

          <h3>Eligibility</h3>
          <p>
            You must be at least 13 years old (or the minimum age of digital consent in your
            country) to use the Service.
          </p>

          <h3>User Responsibility</h3>
          <p>
            You are responsible for the content you upload, submit, or process using our Services.
            Do not submit any content that:
          </p>
          <ul>
            <li>Violates applicable laws or regulations</li>
            <li>Infringes upon intellectual property rights</li>
            <li>Contains harmful, malicious, or illegal material</li>
          </ul>

          <h2>2. Intellectual Property</h2>
          <h3>Ownership</h3>
          <p>
            We retain all rights, title, and interest in and to the Service, including software,
            algorithms, and any related intellectual property.
          </p>

          <h3>User Content</h3>
          <p>
            You retain ownership of any content you submit. By using the Service, you grant us a
            limited, non-exclusive license to process your content for the purpose of providing the
            Services.
          </p>

          <h2>3. Limitations and Restrictions</h2>
          <p>You agree not to:</p>
          <ul>
            <li>Use the Service to generate harmful, deceptive, or illegal content</li>
            <li>Reverse engineer or attempt to extract the source code of the Service</li>
            <li>
              Resell or distribute the summaries or outputs generated for commercial purposes
              without explicit written permission
            </li>
          </ul>

          <h2>4. Disclaimers</h2>
          <p>
            The Service is provided “as is” and “as available,” without warranties of any kind. We
            do not guarantee:
          </p>
          <ul>
            <li>That the summaries will be accurate, complete, or reliable</li>
            <li>That the Service will be uninterrupted or error-free</li>
          </ul>

          <h2>5. Limitation of Liability</h2>
          <p>
            To the fullest extent permitted by law, [Your AI Summarizer Name] shall not be liable
            for any indirect, incidental, special, consequential, or punitive damages, or any loss
            of profits or revenues arising from your use of the Service.
          </p>

          <h2>6. Termination</h2>
          <p>
            We reserve the right to suspend or terminate your access to the Service at our
            discretion, without notice, if we believe you have violated these Terms.
          </p>

          <h2>7. Privacy</h2>
          <p>
            Your privacy is important to us. Please review our
            <a href="#privacy-policy">Privacy Policy</a> for details on how we collect, use, and
            protect your data.
          </p>

          <h2>8. Changes to Terms</h2>
          <p>
            We may modify these Terms at any time. If we make material changes, we will notify you
            via email or through the Service. Continued use of the Service after changes become
            effective constitutes your acceptance of the new Terms.
          </p>

          <h2>9. Governing Law</h2>
          <p>
            These Terms are governed by and construed in accordance with the laws of [Insert
            Jurisdiction], without regard to conflict of law principles.
          </p>

          <h1>Privacy Policy</h1>
          <p><strong>Effective Date:</strong> [Insert Date]</p>

          <p>
            This Privacy Policy explains how [Your AI Summarizer Name] ("we", "us", or "our")
            collects, uses, and protects your information when you use our Services.
          </p>

          <h2>1. Information We Collect</h2>
          <ul>
            <li>
              <strong>User Input:</strong> Text or documents submitted by users for summarization
            </li>
            <li>
              <strong>Usage Data:</strong> Interaction logs, preferences, and other usage statistics
            </li>
            <li>
              <strong>Device Information:</strong> IP address, browser type, operating system, etc.
            </li>
          </ul>

          <h2>2. How We Use Your Information</h2>
          <ul>
            <li>To provide and improve the AI summarization services</li>
            <li>To personalize your experience</li>
            <li>To monitor usage and maintain security</li>
            <li>To comply with legal obligations</li>
          </ul>

          <h2>3. Data Retention</h2>
          <p>
            We retain user-submitted content only as long as necessary to deliver and improve our
            services. You may request deletion of your data by contacting us at [Insert Contact
            Email].
          </p>

          <h2>4. Sharing of Data</h2>
          <p>
            We do not sell or rent your data. We may share information with trusted third-party
            service providers under strict confidentiality agreements, and only as necessary to
            operate and improve our Services.
          </p>

          <h2>5. Security</h2>
          <p>
            We implement reasonable administrative, technical, and physical safeguards to protect
            your information. However, no system can be guaranteed to be 100% secure.
          </p>

          <h2>6. Your Rights</h2>
          <p>
            Depending on your jurisdiction, you may have the right to access, correct, delete, or
            restrict the use of your personal information. To exercise your rights, contact us at
            [Insert Contact Email].
          </p>

          <h2>7. Children's Privacy</h2>
          <p>
            Our Service is not intended for use by children under the age of 13. We do not knowingly
            collect personal data from children.
          </p>

          <h2>8. Changes to This Privacy Policy</h2>
          <p>
            We may update this Privacy Policy from time to time. Material changes will be notified
            through our website or by email.
          </p>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="$emit('close')">OK</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TermsOfServiceDialog',
  emits: ['close'],
}
</script>
